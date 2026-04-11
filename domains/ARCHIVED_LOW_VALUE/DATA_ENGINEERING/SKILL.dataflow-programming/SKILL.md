---
Domain: DATA_ENGINEERING
name: dataflow-programming
Purpose: Build data pipelines and stream processing systems using dataflow programming paradigms
Description: Code patterns for dataflow programming across Google Cloud Dataflow, distributed stream processing (Flink/Spark), and reactive frontend (RxJS)
metadata:
  updated-on: "2026-03-18"
  source: community
  tags: "dataflow,streaming,apache-beam,flink,spark,rxjs,reactive"
---

# Dataflow Programming Skill

Code patterns for building data pipelines and stream processing systems.

---

## Google Cloud Dataflow / Apache Beam

### Basic Pipeline (Python)

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class CountWords(beam.DoFn):
    def process(self, element):
        for word in element.split():
            yield beam.window.GlobalWindows.windowed_value((word, 1))

options = PipelineOptions([
    '--project=my-project',
    '--runner=DataflowRunner',
    '--region=us-central1',
    '--temp_location=gs://my-bucket/temp'
])

with beam.Pipeline(options=options) as p:
    (p
     | 'Read' >> beam.io.ReadFromText('gs://input/*.txt')
     | 'Count' >> beam.ParDo(CountWords())
     | 'Group' >> beam.CombinePerKey(sum)
     | 'Write' >> beam.io.WriteToText('gs://output/result'))
```

### Windowed Streaming (Fixed Windows)

```python
from apache_beam import window
from apache_beam.transforms.trigger import AfterWatermark, AfterProcessingTime, AccumulationMode

class AddTimestamp(beam.DoFn):
    def process(self, element, timestamp=beam.DoFn.TimestampParam):
        yield windowed_value(element, timestamp.to_utc_datetime())

(P
 | 'WithTS' >> beam.ParDo(AddTimestamp())
 | 'Window' >> beam.WindowInto(
     window.FixedWindows(60 * 60),  # 1-hour windows
     trigger=AfterWatermark(early=AfterProcessingTime(10 * 60)),
     accumulation_mode=AccumulationMode.DISCARDING
 )
 | 'Group' >> beam.GroupByKey()
)
```

### ParDo with Side Inputs

```python
class EnrichWithLookup(beam.DoFn):
    def process(self, element, lookup_dict=beam.DoFn.SideInput):
        user_id, event = element
        user_info = lookup_dict.get(user_id, {})
        yield {**event, 'user_name': user_info.get('name', 'unknown')}

lookup = p | 'CreateLookup' >> beam.Create({
    'user_1': {'name': 'Alice', 'tier': 'premium'},
    'user_2': {'name': 'Bob', 'tier': 'free'}
})

(p
 | 'ReadEvents' >> beam.io.ReadFromPubSub(topic='projects/x/topics/events')
 | 'Enrich' >> beam.ParDo(EnrichWithLookup(), lookup_dict=beam.pvalue.AsDict(lookup))
)
```

### Custom Transform (Composite)

```python
class ExtractAndCount(beam.PTransform):
    def __init__(self, field_name):
        self.field_name = field_name
    
    def expand(self, pcoll):
        return (
            pcoll
            | 'Extract' >> beam.FlatMap(lambda x: x.get(self.field_name, []))
            | 'Count' >> beam.combiners.Count.PerElement()
        )

# Usage
events | 'CountTags' >> ExtractAndCount('tags')
```

### Testing with Fake Runner

```python
import unittest
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

class TestWordCount(unittest.TestCase):
    def test_count_words(self):
        inputs = ['hello world', 'hello again']
        expected = [('hello', 2), ('world', 1), ('again', 1)]
        
        with TestPipeline() as p:
            result = (
                p | beam.Create(inputs)
                | beam.FlatMap(lambda x: x.split())
                | beam.combiners.Count.PerElement()
            )
            assert_that(result, equal_to(expected))

if __name__ == '__main__':
    unittest.main()
```

---

## Apache Flink (Scala)

### Basic Stream Job

```scala
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.{TumblingEventTimeWindows, SlidingProcessingTimeWindows}
import org.apache.flink.streaming.api.windowing.time.Time

val env = StreamExecutionEnvironment.getExecutionEnvironment
env.setParallelism(2)

val source: DataStream[String] = env
  .socketTextStream("localhost", 9999)
  .uid("socket-source")

val parsed = source
  .flatMap(_.split(","))
  .filter(_.nonEmpty)
  .map((_, 1))
  .uid("parse-map")

val windowed = parsed
  .keyBy(_._1)
  .window(TumblingEventTimeWindows.of(Time.minutes(5)))
  .sum(1)

windowed.print()
env.execute("WordCount Job")
```

### Keyed Process Function (Stateful)

```scala
class RunningAverage extends KeyedProcessFunction[String, (String, Long), (String, Double)] {
  
  lazy val sumState: ValueState[Long] = getRuntimeContext.getState(
    new ValueStateDescriptor[Long]("sum", classOf[Long])
  )
  lazy val countState: ValueState[Long] = getRuntimeContext.getState(
    new ValueStateDescriptor[Long]("count", classOf[Long])
  )

  override def processElement(
    value: (String, Long),
    ctx: KeyedProcessFunction[String, (String, Long), (String, Double)]#Context,
    out: Collector[(String, Double)]
  ): Unit = {
    val sum = sumState.value() + value._2
    val count = countState.value() + 1
    
    sumState.update(sum)
    countState.update(count)
    
    out.collect((value._1, sum.toDouble / count))
  }
}
```

### Event Time + Watermarks

```scala
import org.apache.flink.streaming.api.functions.timestamps.BoundedOutOfOrdernessTimestampExtractor
import org.apache.flink.api.common.eventtime.{WatermarkStrategy, TimestampAssigner}

case class Event(user: String, value: Long, ts: Long)

val watermarkStrategy = WatermarkStrategy
  .forBoundedOutOfOrderness[Event](Duration.ofSeconds(10))
  .withTimestampAssigner(new TimestampAssigner[Event] {
    override def extractTimestamp(element: Event, recordTimestamp: Long): Long = element.ts
  })

val stream = env
  .addSource(new KafkaSource[Event])
  .assignTimestampsAndWatermarks(watermarkStrategy)
  .keyBy(_.user)
  .window(TumblingEventTimeWindows.of(Time.minutes(5)))
  .reduce((a, b) => Event(a.user, a.value + b.value, a.ts))
```

### Flink SQL Streaming

```scala
import org.apache.flink.table.api._

val settings = EnvironmentSettings.newInstance().inStreamingMode().build()
val tEnv = TableEnvironment.create(settings)

tEnv.executeSql("""
  CREATE TEMPORARY VIEW orders AS
  SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts DESC) as rn
    FROM orders_stream
  ) WHERE rn = 1
""")

tEnv.executeSql("""
  SELECT window_start, window_end, product, SUM(quantity) as total
  FROM TUMBLE(orders, DESCRIPTOR(ts), INTERVAL '1' HOUR)
  GROUP BY window_start, window_end, product
""")
```

---

## Spark Structured Streaming (Scala)

### Basic Streaming Query

```scala
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger

val spark = SparkSession.builder()
  .appName("StreamingWordCount")
  .getOrCreate()

val lines = spark.readStream
  .format("socket")
  .option("host", "localhost")
  .option("port", 9999)
  .load()

val words = lines.select(explode(split($"value", " ")).as("word"))
val counts = words.groupBy("word").count()

val query = counts.writeStream
  .format("console")
  .outputMode("complete")
  .trigger(Trigger.ProcessingTime("10 seconds"))
  .start()

query.awaitTermination()
```

### Watermarked Stream with Late Data

```scala
val events = spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "localhost:9092")
  .option("subscribe", "events")
  .load()
  .select(from_json($"value".cast("string"), schema).as("data"))
  .select($"data.*")

val watermarked = events
  .withWatermark("eventTime", "30 minutes")
  .groupBy(window($"eventTime", "1 hour"), $"productId")
  .agg(sum($"quantity").as("total_sales"))

watermarked.writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation", "s3://checkpoint/")
  .start("s3://output/tables/sales")
```

### Stateful Streaming with mapGroupsWithState

```scala
case class UserSession(userId: String, events: Seq[Event])
case class UserState(userId: String, sessionStart: Long, eventCount: Long, lastEventTime: Long)

val updateSession = (key: String, events: Iterator[Event], state: GroupState[UserState]) => {
  
  if (state.hasTimedOut) {
    state.remove()
    Iterator.empty
  } else {
    val eventsList = events.toSeq
    val newCount = state.getOption.map(_.eventCount).getOrElse(0L) + eventsList.size
    
    val newState = UserState(
      userId = key,
      sessionStart = state.getOption.map(_.sessionStart).getOrElse(System.currentTimeMillis()),
      eventCount = newCount,
      lastEventTime = eventsList.last.timestamp
    )
    
    state.update(newState)
    state.setTimeoutTimestamp(newState.lastEventTime, "30 minutes")
    
    Iterator((key, newState))
  }
}

val sessions = events
  .groupByKey(_.userId)
  .mapGroupsWithState(GroupStateTimeout.EventTimeTimeout())(updateSession)
```

### Streaming Joins

```scala
val impressions = spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "localhost:9092")
  .option("subscribe", "impressions")
  .load()

val clicks = spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "localhost:9092")
  .option("subscribe", "clicks")
  .load()

val joined = impressions
  .withWatermark("timestamp", "1 hour")
  .join(
    clicks.withWatermark("timestamp", "1 hour"),
    expr("adId = clickAdId AND timestamp BETWEEN clickTimestamp - INTERVAL 5 MINUTES AND clickTimestamp + INTERVAL 5 MINUTES")
  )
```

---

## Reactive Frontend (RxJS)

### Basic Observable Stream

```typescript
import { from, Subject, merge, interval } from 'rxjs';
import { map, filter, debounceTime, distinctUntilChanged, switchMap, takeUntil } from 'rxjs/operators';

const search$ = new Subject<string>();

search$.pipe(
  debounceTime(300),
  distinctUntilChanged(),
  filter(term => term.length >= 2),
  switchMap(term => from(api.search(term)))
).subscribe(results => console.log(results));
```

### Stream Transformation Pipeline

```typescript
import { fromEvent, Observable } from 'rxjs';
import { map, scan, throttleTime, bufferTime } from 'rxjs/operators';

const clicks$ = fromEvent<MouseEvent>(document, 'click');

clicks$.pipe(
  throttleTime(1000),
  map(e => ({ x: e.clientX, y: e.clientY, timestamp: Date.now() })),
  scan((acc, curr) => ({
    count: acc.count + 1,
    lastClick: curr,
    clicks: [...acc.clicks, curr].slice(-10)
  }), { count: 0, lastClick: null, clicks: [] as any[] })
).subscribe(state => {
  updateUI(state);
});
```

### Handling Race Conditions with switchMap/cancel

```typescript
import { fromEvent } from 'rxjs';
import { switchMap, catchError, of, delay } from 'rxjs/operators';

const searchInput = document.getElementById('search') as HTMLInputElement;

fromEvent(searchInput, 'input').pipe(
  map((e: any) => e.target.value),
  filter(value => value.length > 0),
  switchMap(query => 
    ajax(`/api/search?q=${query}`).pipe(
      catchError(err => of({ results: [] }))
    )
  )
).subscribe(response => {
  renderResults(response.results);
});
```

### Polling with retry + timer

```typescript
import { timer, of, throwError } from 'rxjs';
import { switchMap, retry, catchError, takeWhile, finalize } from 'rxjs/operators';

let isActive = true;

polling$.pipe(
  switchMap(() => 
    ajax('/api/status').pipe(
      retry({ count: 3, delay: 1000 })
    )
  ),
  takeWhile(response => isActive && response.status === 'ok', true),
  finalize(() => console.log('Polling stopped'))
).subscribe({
  next: data => console.log('Status:', data),
  error: err => console.error('Failed after retries:', err)
});
```

### Custom Operator

```typescript
import { OperatorFunction, Observable } from 'rxjs';

function debug<T>(label: string): OperatorFunction<T, T> {
  return source$ => new Observable(subscriber => {
    return source$.subscribe({
      next: value => {
        console.log(`[${label}] Next:`, value);
        subscriber.next(value);
      },
      error: err => {
        console.error(`[${label}] Error:`, err);
        subscriber.error(err);
      },
      complete: () => {
        console.log(`[${label}] Complete`);
        subscriber.complete();
      }
    });
  });
}

// Usage
data$.pipe(
  debug('input'),
  map(x => x * 2),
  debug('output')
).subscribe();
```

### Managing Subscriptions with takeUntil

```typescript
import { Subject, fromEvent, merge } from 'rxjs';
import { takeUntil, map } from 'rxjs/operators';

const destroy$ = new Subject<void>();

const move$ = fromEvent<MouseEvent>(document, 'mousemove').pipe(
  map(e => ({ x: e.clientX, y: e.clientY }))
);

const up$ = fromEvent(document, 'mouseup');

move$.pipe(
  takeUntil(up$),
  takeUntil(destroy$)
).subscribe(pos => drawAt(pos.x, pos.y));

// On component destroy
ngOnDestroy() {
  destroy$.next();
  destroy$.complete();
}
```

---

## Testing Dataflows

### RxJS Marble Testing

```typescript
import { TestScheduler } from 'rxjs/testing';

it('should debounce and transform', () => {
  const scheduler = new TestScheduler((actual, expected) => {
    expect(actual).toEqual(expected);
  });

  scheduler.run(({ hot, cold, expectObservable }) => {
    const input = hot('  -a--b--c---|', { a: 'he', b: 'hel', c: 'hell' });
    const expected = '  ---a--b--c-|';
    
    const result = input.pipe(
      debounceTime(10, scheduler),
      map(x => x.length)
    );
    
    expectObservable(result).toBe(expected, { a: 2, b: 3, c: 4 });
  });
});
```

### Flink Unit Testing

```scala
import org.apache.flink.streaming.util.KeyedOneInputStreamOperatorTestHarness
import org.apache.flink.streaming.api.functions.KeyedProcessFunction
import org.apache.flink.api.common.state.{ValueState, ValueStateDescriptor}

@Test
def testProcessFunction(): Unit = {
  val harness = new KeyedOneInputStreamOperatorTestHarness(
    new RunningAverage(),
    (x: (String, Long)) => x._1,
    Types.STRING
  )
  
  harness.open()
  
  harness.processElement(("key", 5L), 1000)
  harness.processElement(("key", 7L), 2000)
  
  val result = harness.extractOutputValues()
  assert(result.contains(("key", 5.0)))
  assert(result.contains(("key", 6.0)))
}
```
