#!/usr/bin/env python3
"""
Apache Beam Streaming & Batch Processing

This skill provides comprehensive implementation patterns for distributed data processing
pipelines using Apache Beam with windowing, triggers, and watermarking. It covers both
streaming and batch processing scenarios with proper handling of late data and event time.

Source: Distributed Systems Skills Framework
Type: Advanced Implementation Patterns
Category: Stream Processing
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import apache_beam as beam
from apache_beam import window
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.transforms import trigger
from apache_beam.transforms.window import TimestampedValue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApacheBeamPipelineBuilder:
    """
    A comprehensive class for building Apache Beam pipelines with advanced windowing,
    triggering, and watermarking strategies.
    """
    
    def __init__(self, pipeline_name: str = "beam_pipeline"):
        """
        Initialize the pipeline builder.
        
        Args:
            pipeline_name (str): Name of the pipeline
        """
        self.pipeline_name = pipeline_name
        self.pipeline_options = None
        self.pipeline = None
        self.transforms = []
        
        logger.info(f"Initializing Apache Beam pipeline: {pipeline_name}")
    
    def configure_options(self, runner: str = "DirectRunner", 
                         project: Optional[str] = None,
                         temp_location: Optional[str] = None,
                         streaming: bool = False) -> PipelineOptions:
        """
        Configure pipeline options for different runners and environments.
        
        Args:
            runner (str): Pipeline runner (DirectRunner, DataflowRunner, etc.)
            project (Optional[str]): Google Cloud project ID
            temp_location (Optional[str]): Temporary storage location
            streaming (bool): Whether to run in streaming mode
            
        Returns:
            PipelineOptions: Configured pipeline options
        """
        options = PipelineOptions([
            '--runner=' + runner,
            '--streaming=' + str(streaming).lower()
        ])
        
        if project:
            options.view_as(StandardOptions).project = project
        if temp_location:
            options.view_as(StandardOptions).temp_location = temp_location
        
        self.pipeline_options = options
        logger.info(f"Configured pipeline options: runner={runner}, streaming={streaming}")
        return options
    
    def create_test_stream(self, elements: List[Tuple[Any, float]], 
                          watermark_delay: float = 60.0) -> beam.PTransform:
        """
        Create a test stream for development and testing with proper timestamps.
        
        Args:
            elements (List[Tuple[Any, float]]): List of (data, timestamp) tuples
            watermark_delay (float): Watermark delay in seconds
            
        Returns:
            beam.PTransform: Test stream transform
        """
        test_stream = beam.io.TestStream()
        
        # Add elements with timestamps
        for data, timestamp in elements:
            test_stream = test_stream.advance_watermark_to(timestamp)
            test_stream = test_stream.add_elements([TimestampedValue(data, timestamp)])
        
        # Advance watermark to end
        if elements:
            final_timestamp = max(ts for _, ts in elements)
            test_stream = test_stream.advance_watermark_to(final_timestamp + watermark_delay)
        
        logger.info(f"Created test stream with {len(elements)} elements")
        return test_stream
    
    def create_windowing_strategy(self, window_type: str = "fixed",
                                 window_size: int = 60,
                                 sliding_interval: Optional[int] = None,
                                 session_gap: Optional[int] = None,
                                 allowed_lateness: int = 300,
                                 trigger_type: str = "after_watermark") -> window.WindowFn:
        """
        Create advanced windowing strategies for different use cases.
        
        Args:
            window_type (str): Type of window (fixed, sliding, session)
            window_size (int): Window size in seconds
            sliding_interval (Optional[int]): Sliding interval for sliding windows
            session_gap (Optional[int]): Session gap for session windows
            allowed_lateness (int): Allowed lateness in seconds
            trigger_type (str): Trigger type for window firing
            
        Returns:
            window.WindowFn: Configured window function
        """
        if window_type == "fixed":
            window_fn = window.FixedWindows(window_size)
        elif window_type == "sliding":
            if not sliding_interval:
                raise ValueError("Sliding interval required for sliding windows")
            window_fn = window.SlidingWindows(window_size, sliding_interval)
        elif window_type == "session":
            if not session_gap:
                raise ValueError("Session gap required for session windows")
            window_fn = window.Sessions.with_gap_duration(session_gap)
        else:
            raise ValueError(f"Unknown window type: {window_type}")
        
        # Configure trigger
        if trigger_type == "after_watermark":
            trigger_fn = trigger.AfterWatermark(
                early=trigger.AfterProcessingTime(10),
                late=trigger.AfterCount(1)
            )
        elif trigger_type == "after_count":
            trigger_fn = trigger.AfterCount(100)
        elif trigger_type == "after_processing_time":
            trigger_fn = trigger.AfterProcessingTime(60)
        else:
            trigger_fn = trigger.DefaultTrigger()
        
        # Create windowing strategy
        windowing = window.Windowing(
            window_fn=window_fn,
            trigger=trigger_fn,
            accumulation_mode=trigger.AccumulationMode.ACCUMULATING,
            allowed_lateness=allowed_lateness
        )
        
        logger.info(f"Created {window_type} windowing strategy: size={window_size}s, lateness={allowed_lateness}s")
        return windowing
    
    def create_aggregation_transform(self, aggregation_type: str = "sum",
                                   key_field: str = "key",
                                   value_field: str = "value") -> beam.PTransform:
        """
        Create aggregation transforms for windowed data.
        
        Args:
            aggregation_type (str): Type of aggregation (sum, count, mean, max, min)
            key_field (str): Field to group by
            value_field (str): Field to aggregate
            
        Returns:
            beam.PTransform: Aggregation transform
        """
        def extract_key_value(element):
            if isinstance(element, dict):
                return element.get(key_field, "default"), element.get(value_field, 0)
            elif isinstance(element, tuple) and len(element) == 2:
                return element[0], element[1]
            else:
                return "default", element
        
        def aggregate_values(elements):
            values = list(elements)
            if aggregation_type == "sum":
                return sum(values)
            elif aggregation_type == "count":
                return len(values)
            elif aggregation_type == "mean":
                return sum(values) / len(values) if values else 0
            elif aggregation_type == "max":
                return max(values) if values else 0
            elif aggregation_type == "min":
                return min(values) if values else 0
            else:
                return values
        
        return (beam.Map(extract_key_value) 
                | beam.GroupByKey() 
                | beam.Map(lambda kv: (kv[0], aggregate_values(kv[1]))))
    
    def create_pipeline(self, elements: List[Tuple[Any, float]],
                       window_type: str = "fixed",
                       window_size: int = 60,
                       aggregation_type: str = "sum") -> beam.Pipeline:
        """
        Create a complete Apache Beam pipeline with test data.
        
        Args:
            elements (List[Tuple[Any, float]]): Test data elements
            window_type (str): Window type for aggregation
            window_size (int): Window size in seconds
            aggregation_type (str): Type of aggregation to perform
            
        Returns:
            beam.Pipeline: Configured pipeline
        """
        # Configure pipeline
        self.configure_options(streaming=False)
        
        # Create pipeline
        self.pipeline = beam.Pipeline(options=self.pipeline_options)
        
        # Create test stream
        test_stream = self.create_test_stream(elements)
        
        # Create windowing strategy
        windowing = self.create_windowing_strategy(
            window_type=window_type,
            window_size=window_size
        )
        
        # Create aggregation transform
        aggregation = self.create_aggregation_transform(
            aggregation_type=aggregation_type
        )
        
        # Build pipeline
        (self.pipeline
         | "CreateTestStream" >> test_stream
         | "ApplyWindowing" >> beam.WindowInto(windowing.window_fn)
         | "AggregateData" >> aggregation
         | "FormatOutput" >> beam.Map(lambda kv: f"Window: {kv[0]}, Value: {kv[1]}")
         | "WriteOutput" >> beam.io.WriteToText("output/results"))
        
        logger.info("Pipeline created successfully")
        return self.pipeline
    
    def run_pipeline(self) -> Dict[str, Any]:
        """
        Run the Apache Beam pipeline and return results.
        
        Returns:
            Dict[str, Any]: Pipeline execution results
        """
        if not self.pipeline:
            raise ValueError("Pipeline not created. Call create_pipeline first.")
        
        try:
            result = self.pipeline.run()
            result.wait_until_finish()
            
            logger.info("Pipeline execution completed successfully")
            return {
                "status": "success",
                "pipeline_name": self.pipeline_name,
                "execution_time": "completed"
            }
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "pipeline_name": self.pipeline_name
            }


class StreamingPipelineBuilder(ApacheBeamPipelineBuilder):
    """
    Specialized builder for streaming Apache Beam pipelines with real-time processing.
    """
    
    def __init__(self, pipeline_name: str = "streaming_pipeline"):
        super().__init__(pipeline_name)
    
    def configure_streaming_options(self, project: str, 
                                   subscription: str,
                                   window_size: int = 60,
                                   allowed_lateness: int = 300) -> PipelineOptions:
        """
        Configure options for streaming pipeline with Pub/Sub input.
        
        Args:
            project (str): Google Cloud project ID
            subscription (str): Pub/Sub subscription name
            window_size (int): Window size in seconds
            allowed_lateness (int): Allowed lateness in seconds
            
        Returns:
            PipelineOptions: Configured streaming options
        """
        options = self.configure_options(
            runner="DataflowRunner",
            project=project,
            streaming=True
        )
        
        # Add streaming-specific options
        options.view_as(StandardOptions).streaming = True
        
        logger.info(f"Configured streaming pipeline: project={project}, subscription={subscription}")
        return options
    
    def create_pubsub_source(self, subscription: str) -> beam.PTransform:
        """
        Create Pub/Sub source for streaming data.
        
        Args:
            subscription (str): Pub/Sub subscription name
            
        Returns:
            beam.PTransform: Pub/Sub source transform
        """
        return beam.io.ReadFromPubSub(subscription=subscription)
    
    def create_real_time_aggregation(self, window_size: int = 60,
                                   aggregation_type: str = "sum") -> beam.PTransform:
        """
        Create real-time aggregation pipeline with proper windowing.
        
        Args:
            window_size (int): Window size in seconds
            aggregation_type (str): Type of aggregation
            
        Returns:
            beam.PTransform: Real-time aggregation pipeline
        """
        # Create windowing with early firing
        windowing = self.create_windowing_strategy(
            window_type="fixed",
            window_size=window_size,
            trigger_type="after_watermark"
        )
        
        # Create aggregation
        aggregation = self.create_aggregation_transform(
            aggregation_type=aggregation_type
        )
        
        return (beam.WindowInto(windowing.window_fn)
                | aggregation
                | beam.Map(lambda kv: {
                    "key": kv[0],
                    "value": kv[1],
                    "timestamp": datetime.now().isoformat()
                }))
    
    def create_streaming_pipeline(self, project: str,
                                subscription: str,
                                window_size: int = 60) -> beam.Pipeline:
        """
        Create a complete streaming pipeline.
        
        Args:
            project (str): Google Cloud project ID
            subscription (str): Pub/Sub subscription name
            window_size (int): Window size in seconds
            
        Returns:
            beam.Pipeline: Configured streaming pipeline
        """
        # Configure streaming options
        self.configure_streaming_options(project, subscription, window_size)
        
        # Create pipeline
        self.pipeline = beam.Pipeline(options=self.pipeline_options)
        
        # Create streaming pipeline
        (self.pipeline
         | "ReadFromPubSub" >> self.create_pubsub_source(subscription)
         | "ParseJSON" >> beam.Map(lambda x: json.loads(x.decode('utf-8')))
         | "RealTimeAggregation" >> self.create_real_time_aggregation(window_size)
         | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
             table=f"{project}:analytics.aggregated_data",
             schema="key:STRING,value:FLOAT,timestamp:TIMESTAMP",
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
         ))
        
        logger.info("Streaming pipeline created successfully")
        return self.pipeline


class BatchPipelineBuilder(ApacheBeamPipelineBuilder):
    """
    Specialized builder for batch Apache Beam pipelines with large-scale data processing.
    """
    
    def __init__(self, pipeline_name: str = "batch_pipeline"):
        super().__init__(pipeline_name)
    
    def create_file_source(self, file_pattern: str, 
                          file_format: str = "text") -> beam.PTransform:
        """
        Create file source for batch processing.
        
        Args:
            file_pattern (str): File pattern (e.g., "gs://bucket/data/*.json")
            file_format (str): File format (text, avro, parquet, etc.)
            
        Returns:
            beam.PTransform: File source transform
        """
        if file_format == "text":
            return beam.io.ReadFromText(file_pattern)
        elif file_format == "avro":
            return beam.io.ReadFromAvro(file_pattern)
        elif file_format == "parquet":
            return beam.io.ReadFromParquet(file_pattern)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
    
    def create_batch_aggregation(self, window_size: int = 3600,
                               aggregation_type: str = "sum") -> beam.PTransform:
        """
        Create batch aggregation pipeline with large window sizes.
        
        Args:
            window_size (int): Window size in seconds
            aggregation_type (str): Type of aggregation
            
        Returns:
            beam.PTransform: Batch aggregation pipeline
        """
        # Create large windowing for batch processing
        windowing = self.create_windowing_strategy(
            window_type="fixed",
            window_size=window_size,
            allowed_lateness=86400  # 24 hours for batch processing
        )
        
        # Create aggregation
        aggregation = self.create_aggregation_transform(
            aggregation_type=aggregation_type
        )
        
        return (beam.WindowInto(windowing.window_fn)
                | aggregation
                | beam.Map(lambda kv: {
                    "key": kv[0],
                    "value": kv[1],
                    "window_start": kv[0],  # Simplified for batch
                    "processing_time": datetime.now().isoformat()
                }))
    
    def create_batch_pipeline(self, input_pattern: str,
                             output_path: str,
                             file_format: str = "text",
                             window_size: int = 3600) -> beam.Pipeline:
        """
        Create a complete batch processing pipeline.
        
        Args:
            input_pattern (str): Input file pattern
            output_path (str): Output file path
            file_format (str): Input file format
            window_size (int): Window size in seconds
            
        Returns:
            beam.Pipeline: Configured batch pipeline
        """
        # Configure batch options
        self.configure_options(runner="DataflowRunner")
        
        # Create pipeline
        self.pipeline = beam.Pipeline(options=self.pipeline_options)
        
        # Create batch pipeline
        (self.pipeline
         | "ReadFromFile" >> self.create_file_source(input_pattern, file_format)
         | "ParseData" >> beam.Map(lambda x: json.loads(x) if file_format == "text" else x)
         | "BatchAggregation" >> self.create_batch_aggregation(window_size)
         | "WriteOutput" >> beam.io.WriteToText(output_path))
        
        logger.info("Batch pipeline created successfully")
        return self.pipeline


def create_real_time_analytics_pipeline(project: str,
                                       subscription: str,
                                       window_size: int = 60) -> Dict[str, Any]:
    """
    Create a real-time analytics pipeline using Apache Beam.
    
    Args:
        project (str): Google Cloud project ID
        subscription (str): Pub/Sub subscription name
        window_size (int): Window size in seconds
        
    Returns:
        Dict[str, Any]: Pipeline creation results
    """
    try:
        builder = StreamingPipelineBuilder("real_time_analytics")
        pipeline = builder.create_streaming_pipeline(project, subscription, window_size)
        
        result = builder.run_pipeline()
        
        return {
            "success": True,
            "pipeline_name": "real_time_analytics",
            "project": project,
            "subscription": subscription,
            "window_size": window_size,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Failed to create real-time analytics pipeline: {e}")
        return {
            "success": False,
            "error": str(e),
            "pipeline_name": "real_time_analytics"
        }


def create_batch_processing_pipeline(input_pattern: str,
                                    output_path: str,
                                    file_format: str = "text",
                                    window_size: int = 3600) -> Dict[str, Any]:
    """
    Create a batch processing pipeline using Apache Beam.
    
    Args:
        input_pattern (str): Input file pattern
        output_path (str): Output file path
        file_format (str): Input file format
        window_size (int): Window size in seconds
        
    Returns:
        Dict[str, Any]: Pipeline creation results
    """
    try:
        builder = BatchPipelineBuilder("batch_processing")
        pipeline = builder.create_batch_pipeline(input_pattern, output_path, file_format, window_size)
        
        result = builder.run_pipeline()
        
        return {
            "success": True,
            "pipeline_name": "batch_processing",
            "input_pattern": input_pattern,
            "output_path": output_path,
            "file_format": file_format,
            "window_size": window_size,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Failed to create batch processing pipeline: {e}")
        return {
            "success": False,
            "error": str(e),
            "pipeline_name": "batch_processing"
        }


def validate_pipeline_configuration(config: Dict[str, Any]) -> bool:
    """
    Validate Apache Beam pipeline configuration.
    
    Args:
        config (Dict[str, Any]): Pipeline configuration
        
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    required_fields = ["pipeline_name", "window_size", "aggregation_type"]
    
    for field in required_fields:
        if field not in config:
            logger.error(f"Missing required field: {field}")
            return False
    
    # Validate window size
    if config["window_size"] <= 0:
        logger.error("Window size must be positive")
        return False
    
    # Validate aggregation type
    valid_aggregations = ["sum", "count", "mean", "max", "min"]
    if config["aggregation_type"] not in valid_aggregations:
        logger.error(f"Invalid aggregation type: {config['aggregation_type']}")
        return False
    
    logger.info("Pipeline configuration validation passed")
    return True


def main():
    """Main execution function demonstrating Apache Beam pipeline creation."""
    print("Apache Beam Streaming & Batch Processing")
    print("=" * 50)
    
    # Example 1: Real-time analytics pipeline
    print("\n1. Creating Real-time Analytics Pipeline...")
    rt_result = create_real_time_analytics_pipeline(
        project="my-gcp-project",
        subscription="projects/my-gcp-project/subscriptions/analytics-sub",
        window_size=60
    )
    
    if rt_result["success"]:
        print("✅ Real-time pipeline created successfully")
    else:
        print(f"❌ Real-time pipeline failed: {rt_result['error']}")
    
    # Example 2: Batch processing pipeline
    print("\n2. Creating Batch Processing Pipeline...")
    batch_result = create_batch_processing_pipeline(
        input_pattern="gs://my-bucket/data/*.json",
        output_path="gs://my-bucket/output/results",
        file_format="text",
        window_size=3600
    )
    
    if batch_result["success"]:
        print("✅ Batch pipeline created successfully")
    else:
        print(f"❌ Batch pipeline failed: {batch_result['error']}")
    
    # Example 3: Test stream pipeline
    print("\n3. Creating Test Stream Pipeline...")
    try:
        builder = ApacheBeamPipelineBuilder("test_stream")
        
        # Create test data
        test_elements = [
            ("event1", 1640995200.0),  # 2022-01-01 00:00:00 UTC
            ("event2", 1640995260.0),  # 2022-01-01 00:01:00 UTC
            ("event3", 1640995320.0),  # 2022-01-01 00:02:00 UTC
        ]
        
        pipeline = builder.create_pipeline(
            elements=test_elements,
            window_type="fixed",
            window_size=60,
            aggregation_type="count"
        )
        
        result = builder.run_pipeline()
        
        if result["status"] == "success":
            print("✅ Test stream pipeline executed successfully")
        else:
            print(f"❌ Test stream pipeline failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Test stream pipeline failed: {e}")
    
    print("\n" + "=" * 50)
    print("Apache Beam pipeline examples completed!")


if __name__ == "__main__":
    main()
