---
name: data-pipeline-orchestrator
description: "Use when: building ETL pipelines, moving data between systems, scheduling data jobs, orchestrating data workflows, or managing data transformations. Triggers: 'ETL', 'data pipeline', 'extract transform load', 'airflow', 'schedule', 'batch', 'data sync', 'data migration', 'data warehouse', 'dbt'. NOT for: real-time streaming (use streaming skills), or ad-hoc queries (use database skills)."
---

# Data Pipeline Orchestrator

Builds and executes data pipelines with ETL operations, error handling, and monitoring.

## Dependencies

- May require `skillsmp-api-client` for discovering data processing skills

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Data Pipeline                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │ Extract│ -> │ Transform│ -> │ Validate│ -> │  Load │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│       │              │             │             │               │
│       v              v             v             v               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Error Handling & Recovery                   │    │
│  │  • Retry logic    • Dead letter queue   • Logging       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### Extract Stage

```python
class DataExtractor:
    def __init__(self, source: DataSource):
        self.source = source
        
    def extract(self) -> RawData:
        """Extract data from source."""
        if self.source.type == "api":
            return self.extract_from_api()
        elif self.source.type == "database":
            return self.extract_from_db()
        elif self.source.type == "file":
            return self.extract_from_file()
        elif self.source.type == "stream":
            return self.extract_from_stream()
            
    def extract_from_api(self) -> RawData:
        """Fetch from REST/GraphQL API."""
        response = self.client.get(self.source.url)
        return RawData(content=response.json())
        
    def extract_from_db(self) -> RawData:
        """Query database."""
        with self.source.connection as conn:
            return RawData(data=pd.read_sql(self.source.query, conn))
```

### Transform Stage

```python
class DataTransformer:
    def __init__(self, transformations: List[Transform]):
        self.transformations = transformations
        
    def transform(self, data: RawData) -> TransformedData:
        """Apply transformations in sequence."""
        result = data
        for transform in self.transformations:
            result = transform.apply(result)
        return result

class Transformations:
    @staticmethod
    def clean_nulls(data: RawData) -> TransformedData:
        """Remove null values."""
        return data.dropna()
        
    @staticmethod
    def normalize_columns(data: RawData) -> TransformedData:
        """Normalize column names and types."""
        return data.rename(columns=str.lower).astype({"age": int})
        
    @staticmethod
    def add_derived_fields(data: RawData) -> TransformedData:
        """Add computed columns."""
        data["total"] = data["quantity"] * data["price"]
        return data
        
    @staticmethod
    def aggregate(data: TransformedData) -> TransformedData:
        """Aggregate by key."""
        return data.groupby("category").agg({"total": "sum"})
```

### Validation Stage

```python
class DataValidator:
    def __init__(self, rules: List[ValidationRule]):
        self.rules = rules
        
    def validate(self, data: TransformedData) -> ValidationResult:
        """Run all validation rules."""
        errors = []
        for rule in self.rules:
            if not rule.check(data):
                errors.append(rule.error_message)
        return ValidationResult(valid=len(errors) == 0, errors=errors)

class ValidationRules:
    @staticmethod
    def required_columns(columns: List[str]) -> ValidationRule:
        return ValidationRule(
            check=lambda d: all(c in d.columns for c in columns),
            error="Missing required columns"
        )
        
    @staticmethod
    def no_duplicates(key: str) -> ValidationRule:
        return ValidationRule(
            check=lambda d: d[key].duplicated().sum() == 0,
            error=f"Duplicate values in {key}"
        )
        
    @staticmethod
    def value_range(column: str, min_val, max_val) -> ValidationRule:
        return ValidationRule(
            check=lambda d: d[column].between(min_val, max_val).all(),
            error=f"{column} values out of range"
        )
```

### Load Stage

```python
class DataLoader:
    def __init__(self, target: DataTarget):
        self.target = target
        
    def load(self, data: TransformedData) -> LoadResult:
        """Load data to destination."""
        if self.target.type == "database":
            return self.load_to_db(data)
        elif self.target.type == "file":
            return self.load_to_file(data)
        elif self.target.type == "api":
            return self.load_to_api(data)
            
    def load_to_db(self, data: TransformedData) -> LoadResult:
        """Bulk insert to database."""
        rows = data.to_dict(orient="records")
        self.target.bulk_insert(rows)
        return LoadResult(rows=len(rows))
```

## Pipeline Orchestration

```python
class PipelineOrchestrator:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.extractor = DataExtractor(config.source)
        self.transformer = DataTransformer(config.transforms)
        self.validator = DataValidator(config.validations)
        self.loader = DataLoader(config.target)
        
    def execute(self) -> PipelineResult:
        """Execute full pipeline with error handling."""
        try:
            # Extract
            raw = self.extractor.extract()
            self.log(f"Extracted {len(raw)} records")
            
            # Transform
            transformed = self.transformer.transform(raw)
            self.log(f"Transformed to {len(transformed)} records")
            
            # Validate
            validation = self.validator.validate(transformed)
            if not validation.valid:
                self.handle_validation_errors(validation.errors)
                
            # Load
            result = self.loader.load(transformed)
            self.log(f"Loaded {result.rows} records")
            
            return PipelineResult(success=True, records=result.rows)
            
        except Exception as e:
            return self.handle_error(e)
            
    def handle_error(self, error: Exception) -> PipelineResult:
        """Retry logic and error handling."""
        for attempt in range(self.config.max_retries):
            try:
                self.log(f"Retry attempt {attempt + 1}")
                return self.execute()
            except Exception:
                if attempt == self.config.max_retries - 1:
                    self.send_alert(error)
                    return PipelineResult(success=False, error=str(error))
                    
    def send_alert(self, error: Exception):
        """Send notification on failure."""
        if self.config.alert_webhook:
            requests.post(self.config.alert_webhook, json={
                "pipeline": self.config.name,
                "error": str(error),
                "timestamp": datetime.now().isoformat()
            })
```

## Configuration

```python
@dataclass
class PipelineConfig:
    name: str
    source: DataSource
    target: DataTarget
    transforms: List[Transform]
    validations: List[ValidationRule]
    max_retries: int = 3
    alert_webhook: Optional[str] = None

@dataclass  
class DataSource:
    type: str  # api, database, file, stream
    url: str
    query: Optional[str] = None
    credentials: Optional[dict] = None
    
@dataclass
class DataTarget:
    type: str  # database, file, api
    connection: str
    table: Optional[str] = None
```

## Usage Example

```python
config = PipelineConfig(
    name="sales-etl",
    source=DataSource(
        type="api",
        url="https://api.sales.example.com/orders"
    ),
    target=DataTarget(
        type="database",
        connection="postgresql://localhost/dw",
        table="fact_sales"
    ),
    transforms=[
        Transformations.clean_nulls,
        Transformations.normalize_columns,
        Transformations.add_derived_fields,
    ],
    validations=[
        ValidationRules.required_columns(["order_id", "amount"]),
        ValidationRules.no_duplicates("order_id"),
    ],
    alert_webhook="https://hooks.example.com/pipeline-alerts"
)

pipeline = PipelineOrchestrator(config)
result = pipeline.execute()

print(f"Pipeline {'succeeded' if result.success else 'failed'}")
```

## Scheduling

For periodic execution, use with a scheduler:

```python
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(
    lambda: PipelineOrchestrator(config).execute(),
    "cron",
    hour=2,  # Run at 2 AM
    day="mon-fri"
)
scheduler.start()
```

## Constraints

- MUST implement retry logic for transient failures
- SHOULD validate data at each stage
- MUST log all operations for debugging
- SHOULD send alerts on pipeline failure
- MAY implement checkpointing for long-running pipelines
- SHOULD handle backpressure in stream processing