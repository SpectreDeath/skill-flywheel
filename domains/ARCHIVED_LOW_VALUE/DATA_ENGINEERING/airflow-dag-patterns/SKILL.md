---
name: airflow-dag-patterns
description: "Use when: building production Apache Airflow DAGs, creating data pipelines, orchestrating workflows, scheduling batch jobs, or implementing Airflow best practices. Triggers: 'Airflow', 'DAG', 'data pipeline', 'workflow', 'scheduler', 'batch job', 'orchestration', 'task'. NOT for: real-time streaming (use Kafka/Flink), simple scripts without scheduling needs, or when using other orchestrators."
---

# Airflow DAG Patterns

Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment.

## When to Use This Skill

Use this skill when:
- Creating data pipelines and ETL workflows
- Scheduling recurring batch jobs
- Orchestrating multi-step processes
- Building dependencies between tasks
- Setting up Airflow from scratch

Do NOT use when:
- Real-time streaming processing
- Simple one-off scripts
- Event-driven workflows (use temporal)
-Microservices orchestration (use Kafka)

## Basic DAG Structure

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline',
    schedule_interval='0 6 * * *',  # Daily at 6 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'daily'],
) as dag:
    
    extract = BashOperator(
        task_id='extract',
        bash_command='python scripts/extract.py',
    )
    
    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
        op_kwargs={'date': '{{ ds }}'},
    )
    
    load = PythonOperator(
        task_id='load',
        python_callable=load_data,
    )
    
    extract >> transform >> load
```

## Task Dependencies

### Linear Dependencies
```python
task1 >> task2 >> task3
```

### Branching
```python
[task1, task2] >> task3
task3 >> [task4, task5]
```

### Cross-DAG Dependencies
```python
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

trigger_downstream = TriggerDagRunOperator(
    task_id='trigger_downstream',
    trigger_dag_id='downstream_dag',
    conf={'date': '{{ ds }}'},
)
```

## Operators

### Python Operator
```python
def process_data(**context):
    execution_date = context['execution_date']
    data = extract_data(execution_date)
    result = transform_data(data)
    load_data(result)
    return result

process = PythonOperator(
    task_id='process',
    python_callable=process_data,
    provide_context=True,
    templates_dict={'date': '{{ ds }}'},
)
```

### SQL Operator
```python
from airflow.operators.sql import SQLExecuteQueryOperator

create_table = SQLExecuteQueryOperator(
    task_id='create_table',
    sql="""
        CREATE TABLE IF NOT EXISTS metrics (
            date DATE,
            revenue DECIMAL(10,2),
            orders INTEGER
        )
    """,
    conn_id='postgres_warehouse',
)
```

### Docker Operator
```python
from airflow.providers.docker.operators.docker import DockerOperator

process_container = DockerOperator(
    task_id='process_container',
    image='data-processor:latest',
    command='python process.py --date {{ ds }}',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
)
```

### Kubernetes Operator
```python
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

run_pod = KubernetesPodOperator(
    task_id='run_pod',
    image='data-processor:latest',
    cmds=['python', 'process.py'],
    arguments=['--date', '{{ ds }}'],
    namespace='data',
    name='process-pod',
    get_logs=True,
)
```

## Sensors

### File Sensor
```python
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id='wait_for_file',
    filepath='/data/incoming/{{ ds }}/file.csv',
    fs_conn_id='filesystem',
    poke_interval=60,
    timeout=3600,
)
```

### External Task Sensor
```python
from airflow.sensors.external_task import ExternalTaskSensor

wait_upstream = ExternalTaskSensor(
    task_id='wait_upstream',
    external_dag_id='upstream_dag',
    external_task_id='complete',
    execution_date_fn=lambda dt: dt,
    timeout=7200,
)
```

### SQL Sensor
```python
from airflow.providers.sqlite.operators.sqlite import SqlSensor

check_data = SqlSensor(
    task_id='check_data',
    sql="SELECT COUNT(*) FROM staging WHERE processed = 0",
    conn_id='warehouse',
    poke_interval=300,
    timeout=3600,
)
```

## XCom for Task Communication

### Push and Pull
```python
# Push from task A
def push_data(**context):
    context['ti'].xcom_push(key='result', value={'count': 100, 'sum': 5000})

task_a = PythonOperator(
    task_id='push',
    python_callable=push_data,
)

# Pull in task B
def pull_data(**context):
    result = context['ti'].xcom_pull(key='result', task_ids='push')
    return result['count']

task_b = PythonOperator(
    task_id='pull',
    python_callable=pull_data,
    provide_context=True,
)

task_a >> task_b
```

## SubDAGs for Reusability

```python
from airflow.models import SubDagOperator

def create_subdag(parent_dag_name, child_dag_name, args):
    dag = DAG(
        f'{parent_dag_name}.{child_dag_name}',
        default_args=args,
        schedule_interval=None,
    )
    
    task1 = BashOperator(
        task_id='step1',
        bash_command='echo step1',
        dag=dag,
    )
    task2 = BashOperator(
        task_id='step2',
        bash_command='echo step2',
        dag=dag,
    )
    task1 >> task2
    return dag

subdag = SubDagOperator(
    task_id='subdag',
    subdag=create_subdag('parent', 'subdag', default_args),
    dag=parent_dag,
)
```

## Task Groups

```python
from airflow.utils.task_group import TaskGroup

with TaskGroup('etl_group') as tg:
    extract = BashOperator(task_id='extract', bash_command='echo extract')
    transform = BashOperator(task_id='transform', bash_command='echo transform')
    load = BashOperator(task_id='load', bash_command='echo load')
    
    extract >> transform >> load
```

## SLAs and Alerts

```python
def send_alert(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    print(f"Task {task_id} in DAG {dag_id} missed SLA")

with DAG(
    'with_sla',
    sla_miss_callback=send_alert,
    default_args=default_args,
) as dag:
    task = PythonOperator(
        task_id='long_running',
        python_callable=long_running_task,
        sla=timedelta(hours=2),
    )
```

## Testing DAGs

### DAG Validation Test
```python
import pytest
from airflow.models import DAG
from airflow.utils.state import State

def test_dag_structure():
    from your_dag import dag
    
    assert dag.dag_id == 'your_dag'
    assert len(dag.tasks) == 3
    
    # Check task dependencies
    task_ids = [t.task_id for t in dag.tasks]
    assert 'extract' in task_ids
    assert 'transform' in task_ids
    assert 'load' in task_ids

def test_task_dependencies():
    from your_dag import dag
    
    extract = dag.get_task('extract')
    transform = dag.get_task('transform')
    
    assert transform in extract.downstream_list
```

### Unit Test for Operator
```python
def test_python_operator():
    from airflow.operators.python import PythonOperator
    
    def my_func():
        return "result"
    
    op = PythonOperator(
        task_id='test',
        python_callable=my_func,
    )
    
    result = op.execute({})
    assert result == "result"
```

## Best Practices

1. **Idempotency**: Tasks should produce same result on re-run
2. **Retries**: Configure for transient failures
3. **Resources**: Set pool and resources appropriately
4. **Logging**: Use proper logging in Python operators
5. **Monitoring**: Set SLAs and alerts
6. **Documentation**: Add docstrings to DAGs
7. **Versioning**: Use sensible start_date
8. **Cleanup**: Clear old DAG runs

## Common Commands

```bash
# List DAGs
airflow dags list

# Show DAG structure
airflow tasks show <dag_id>

# Run DAG manually
airflow dags trigger -e 2024-01-01 <dag_id>

# Backfill
airflow dags backfill -s 2024-01-01 -e 2024-01-31 <dag_id>

# Test task
airflow tasks test <dag_id> <task_id> 2024-01-01
```

## Constraints

- Never set `depends_on_past=True` without careful thought
- Avoid cross-DAG dependencies when possible
- Use TaskGroups for visual organization
- Keep DAGs simple - extract complex logic to operators
- Configure timeouts to prevent stuck tasks
- Use pools for resource management
