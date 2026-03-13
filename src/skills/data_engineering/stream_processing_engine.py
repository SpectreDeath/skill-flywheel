#!/usr/bin/env python3
"""
Skill: stream-processing-engine
Domain: data_engineering
Description: Real-time stream processing engine for continuous data workflows
"""

import asyncio
import logging
import time
import uuid
import json
from typing import Dict, Any, List, Optional, Union, Callable, AsyncGenerator
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import statistics
from collections import deque, defaultdict

logger = logging.getLogger(__name__)

class StreamType(Enum):
    """Types of data streams"""
    KAFKA = "kafka"
    RABBITMQ = "rabbitmq"
    REDIS_STREAM = "redis_stream"
    CUSTOM = "custom"

class ProcessingMode(Enum):
    """Stream processing modes"""
    EXACTLY_ONCE = "exactly_once"
    AT_LEAST_ONCE = "at_least_once"
    AT_MOST_ONCE = "at_most_once"

class WindowType(Enum):
    """Types of time windows"""
    TUMBLING = "tumbling"      # Fixed, non-overlapping windows
    SLIDING = "sliding"       # Overlapping windows
    SESSION = "session"       # Gaps-based windows

@dataclass
class StreamSource:
    """Represents a stream data source"""
    source_id: str
    name: str
    stream_type: StreamType
    connection_config: Dict[str, Any]
    topic: str
    partition: Optional[int]
    offset: Optional[int]
    created_at: float

@dataclass
class StreamProcessor:
    """Represents a stream processor"""
    processor_id: str
    name: str
    processing_mode: ProcessingMode
    window_type: WindowType
    window_size: int  # milliseconds
    slide_interval: int  # milliseconds for sliding windows
    processing_function: Callable
    created_at: float

@dataclass
class StreamSink:
    """Represents a stream data sink"""
    sink_id: str
    name: str
    stream_type: StreamType
    connection_config: Dict[str, Any]
    topic: str
    created_at: float

@dataclass
class StreamEvent:
    """Represents a stream event"""
    event_id: str
    source_id: str
    timestamp: float
    data: Dict[str, Any]
    partition: Optional[int]
    offset: Optional[int]

@dataclass
class StreamWindow:
    """Represents a time window for stream processing"""
    window_id: str
    start_time: float
    end_time: float
    events: List[StreamEvent]
    aggregated_result: Optional[Dict[str, Any]]
    processed_at: Optional[float]

class StreamProcessingEngine:
    """Real-time stream processing engine"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the stream processing engine
        
        Args:
            config: Configuration dictionary with:
                - max_window_size: Maximum window size in milliseconds
                - buffer_size: Event buffer size
                - checkpoint_interval: Checkpoint interval in seconds
        """
        self.max_window_size = config.get("max_window_size", 3600000)  # 1 hour
        self.buffer_size = config.get("buffer_size", 10000)
        self.checkpoint_interval = config.get("checkpoint_interval", 60)
        
        self.stream_sources: Dict[str, StreamSource] = {}
        self.stream_processors: Dict[str, StreamProcessor] = {}
        self.stream_sinks: Dict[str, StreamSink] = {}
        
        self.event_buffer: deque = deque(maxlen=self.buffer_size)
        self.windows: Dict[str, StreamWindow] = {}
        self.checkpoints: Dict[str, Dict[str, Any]] = {}
        
        self.processing_stats = {
            "total_events": 0,
            "processed_events": 0,
            "failed_events": 0,
            "throughput": 0.0,
            "latency": 0.0,
            "active_windows": 0
        }
        
        self.active_processors = {}
        self.processor_tasks = {}
        
        self.logger = logging.getLogger(__name__)
        
        # Start background processing
        self._processing_task = asyncio.create_task(self._processing_loop())
        self._checkpoint_task = asyncio.create_task(self._checkpoint_loop())
    
    def create_stream_source(self,
                           name: str,
                           stream_type: StreamType,
                           connection_config: Dict[str, Any],
                           topic: str,
                           partition: Optional[int] = None,
                           offset: Optional[int] = None) -> str:
        """
        Create a stream data source
        
        Args:
            name: Source name
            stream_type: Type of stream
            connection_config: Connection configuration
            topic: Stream topic
            partition: Specific partition (optional)
            offset: Starting offset (optional)
            
        Returns:
            Source ID
        """
        source_id = str(uuid.uuid4())
        
        source = StreamSource(
            source_id=source_id,
            name=name,
            stream_type=stream_type,
            connection_config=connection_config,
            topic=topic,
            partition=partition,
            offset=offset,
            created_at=time.time()
        )
        
        self.stream_sources[source_id] = source
        self.logger.info(f"Created stream source: {source_id}")
        
        return source_id
    
    def create_stream_processor(self,
                               name: str,
                               processing_mode: ProcessingMode,
                               window_type: WindowType,
                               window_size: int,
                               processing_function: Callable,
                               slide_interval: Optional[int] = None) -> str:
        """
        Create a stream processor
        
        Args:
            name: Processor name
            processing_mode: Processing guarantee mode
            window_type: Type of time window
            window_size: Window size in milliseconds
            processing_function: Function to process events
            slide_interval: Slide interval for sliding windows
            
        Returns:
            Processor ID
        """
        processor_id = str(uuid.uuid4())
        
        processor = StreamProcessor(
            processor_id=processor_id,
            name=name,
            processing_mode=processing_mode,
            window_type=window_type,
            window_size=window_size,
            slide_interval=slide_interval or window_size,
            processing_function=processing_function,
            created_at=time.time()
        )
        
        self.stream_processors[processor_id] = processor
        self.logger.info(f"Created stream processor: {processor_id}")
        
        return processor_id
    
    def create_stream_sink(self,
                          name: str,
                          stream_type: StreamType,
                          connection_config: Dict[str, Any],
                          topic: str) -> str:
        """
        Create a stream data sink
        
        Args:
            name: Sink name
            stream_type: Type of stream
            connection_config: Connection configuration
            topic: Stream topic
            
        Returns:
            Sink ID
        """
        sink_id = str(uuid.uuid4())
        
        sink = StreamSink(
            sink_id=sink_id,
            name=name,
            stream_type=stream_type,
            connection_config=connection_config,
            topic=topic,
            created_at=time.time()
        )
        
        self.stream_sinks[sink_id] = sink
        self.logger.info(f"Created stream sink: {sink_id}")
        
        return sink_id
    
    async def start_stream_processing(self, 
                                    source_id: str,
                                    processor_id: str,
                                    sink_id: Optional[str] = None) -> str:
        """
        Start stream processing for a source-processor pair
        
        Args:
            source_id: Source ID
            processor_id: Processor ID
            sink_id: Optional sink ID
            
        Returns:
            Processing session ID
        """
        if source_id not in self.stream_sources:
            raise ValueError(f"Source {source_id} not found")
        
        if processor_id not in self.stream_processors:
            raise ValueError(f"Processor {processor_id} not found")
        
        session_id = str(uuid.uuid4())
        
        # Create processing session
        session_config = {
            "session_id": session_id,
            "source_id": source_id,
            "processor_id": processor_id,
            "sink_id": sink_id,
            "started_at": time.time(),
            "status": "running"
        }
        
        self.active_processors[session_id] = session_config
        
        # Start processing task
        task = asyncio.create_task(self._process_stream_events(session_id, session_config))
        self.processor_tasks[session_id] = task
        
        self.logger.info(f"Started stream processing: {session_id}")
        return session_id
    
    async def stop_stream_processing(self, session_id: str):
        """Stop stream processing for a session"""
        if session_id in self.processor_tasks:
            self.processor_tasks[session_id].cancel()
            del self.processor_tasks[session_id]
        
        if session_id in self.active_processors:
            self.active_processors[session_id]["status"] = "stopped"
            self.active_processors[session_id]["stopped_at"] = time.time()
    
    async def ingest_event(self, source_id: str, data: Dict[str, Any]) -> str:
        """
        Ingest a stream event
        
        Args:
            source_id: Source ID
            data: Event data
            
        Returns:
            Event ID
        """
        if source_id not in self.stream_sources:
            raise ValueError(f"Source {source_id} not found")
        
        event_id = str(uuid.uuid4())
        
        event = StreamEvent(
            event_id=event_id,
            source_id=source_id,
            timestamp=time.time(),
            data=data,
            partition=None,  # Would be set by actual stream source
            offset=None     # Would be set by actual stream source
        )
        
        self.event_buffer.append(event)
        self.processing_stats["total_events"] += 1
        
        # Trigger window processing
        await self._process_windows(event)
        
        return event_id
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get stream processing statistics"""
        return {
            "total_events": self.processing_stats["total_events"],
            "processed_events": self.processing_stats["processed_events"],
            "failed_events": self.processing_stats["failed_events"],
            "throughput": self.processing_stats["throughput"],
            "latency": self.processing_stats["latency"],
            "active_windows": len(self.windows),
            "active_processors": len(self.active_processors),
            "buffer_size": len(self.event_buffer),
            "max_window_size": self.max_window_size,
            "checkpoint_interval": self.checkpoint_interval
        }
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get list of active processing sessions"""
        return list(self.active_processors.values())
    
    async def _processing_loop(self):
        """Background processing loop"""
        while True:
            try:
                await self._process_buffer()
                await asyncio.sleep(0.1)  # Process every 100ms
            except Exception as e:
                self.logger.error(f"Error in processing loop: {e}")
                await asyncio.sleep(1)
    
    async def _process_buffer(self):
        """Process events in the buffer"""
        current_time = time.time()
        
        # Process events that are ready
        events_to_process = []
        for event in self.event_buffer:
            # Check if event should be processed based on window logic
            if self._should_process_event(event, current_time):
                events_to_process.append(event)
        
        # Remove processed events from buffer
        for event in events_to_process:
            if event in self.event_buffer:
                self.event_buffer.remove(event)
    
    def _should_process_event(self, event: StreamEvent, current_time: float) -> bool:
        """Determine if an event should be processed"""
        # Simple heuristic: process if event is older than 1 second
        # In a real implementation, this would be based on window logic
        return (current_time - event.timestamp) > 1.0
    
    async def _process_windows(self, event: StreamEvent):
        """Process time windows for an event"""
        current_time = time.time()
        
        # Create or update windows based on event timestamp
        for processor_id, processor in self.stream_processors.items():
            window_key = f"{processor_id}_{int(current_time // processor.window_size)}"
            
            if window_key not in self.windows:
                window = StreamWindow(
                    window_id=window_key,
                    start_time=current_time - processor.window_size,
                    end_time=current_time,
                    events=[],
                    aggregated_result=None,
                    processed_at=None
                )
                self.windows[window_key] = window
            
            self.windows[window_key].events.append(event)
            
            # Check if window should be processed
            if self._should_process_window(self.windows[window_key], current_time):
                await self._process_window(self.windows[window_key], processor)
    
    def _should_process_window(self, window: StreamWindow, current_time: float) -> bool:
        """Determine if a window should be processed"""
        # Process window if it's complete or if enough time has passed
        return current_time >= window.end_time or len(window.events) >= 100
    
    async def _process_window(self, window: StreamWindow, processor: StreamProcessor):
        """Process a time window"""
        try:
            # Get processor function
            processing_func = processor.processing_function
            
            # Prepare window data
            window_data = {
                "window_id": window.window_id,
                "start_time": window.start_time,
                "end_time": window.end_time,
                "events": [event.data for event in window.events],
                "event_count": len(window.events)
            }
            
            # Process window
            result = processing_func(window_data)
            
            # Store result
            window.aggregated_result = result
            window.processed_at = time.time()
            
            # Update statistics
            self.processing_stats["processed_events"] += len(window.events)
            self.processing_stats["throughput"] = self.processing_stats["processed_events"] / max(1, time.time() - window.start_time)
            
            self.logger.info(f"Processed window {window.window_id}: {len(window.events)} events")
            
        except Exception as e:
            self.processing_stats["failed_events"] += len(window.events)
            self.logger.error(f"Error processing window {window.window_id}: {e}")
    
    async def _process_stream_events(self, session_id: str, session_config: Dict[str, Any]):
        """Process events for a specific stream session"""
        source_id = session_config["source_id"]
        processor_id = session_config["processor_id"]
        sink_id = session_config.get("sink_id")
        
        processor = self.stream_processors[processor_id]
        
        # Simulate stream processing
        while session_id in self.active_processors:
            try:
                # Get events for this source
                source_events = [e for e in self.event_buffer if e.source_id == source_id]
                
                if source_events:
                    # Process events in batches
                    batch_size = min(100, len(source_events))
                    batch = source_events[:batch_size]
                    
                    # Create window for batch
                    window_data = {
                        "window_id": f"batch_{time.time()}",
                        "start_time": time.time(),
                        "end_time": time.time(),
                        "events": [e.data for e in batch],
                        "event_count": len(batch)
                    }
                    
                    # Process batch
                    result = processor.processing_function(window_data)
                    
                    # Send to sink if configured
                    if sink_id and sink_id in self.stream_sinks:
                        await self._send_to_sink(sink_id, result)
                    
                    # Remove processed events
                    for event in batch:
                        if event in self.event_buffer:
                            self.event_buffer.remove(event)
                    
                    self.processing_stats["processed_events"] += len(batch)
                
                await asyncio.sleep(0.5)  # Process every 500ms
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in stream processing {session_id}: {e}")
                await asyncio.sleep(1)
    
    async def _send_to_sink(self, sink_id: str, data: Dict[str, Any]):
        """Send processed data to sink"""
        sink = self.stream_sinks[sink_id]
        
        # Simulate sending to sink
        await asyncio.sleep(0.1)
        
        self.logger.info(f"Sent data to sink {sink_id}: {len(str(data))} bytes")
    
    async def _checkpoint_loop(self):
        """Background checkpoint loop"""
        while True:
            try:
                await self._create_checkpoint()
                await asyncio.sleep(self.checkpoint_interval)
            except Exception as e:
                self.logger.error(f"Error in checkpoint loop: {e}")
                await asyncio.sleep(self.checkpoint_interval)
    
    async def _create_checkpoint(self):
        """Create a checkpoint of current state"""
        checkpoint_data = {
            "timestamp": time.time(),
            "event_buffer_size": len(self.event_buffer),
            "windows_count": len(self.windows),
            "processing_stats": self.processing_stats.copy(),
            "active_processors": len(self.active_processors)
        }
        
        checkpoint_id = str(uuid.uuid4())
        self.checkpoints[checkpoint_id] = checkpoint_data
        
        # Keep only last 10 checkpoints
        if len(self.checkpoints) > 10:
            oldest_checkpoint = min(self.checkpoints.keys(), key=lambda k: self.checkpoints[k]["timestamp"])
            del self.checkpoints[oldest_checkpoint]
        
        self.logger.info(f"Created checkpoint: {checkpoint_id}")

# Global stream processing engine instance
_stream_engine = StreamProcessingEngine({})

# Example processing functions
def aggregate_sales_data(window_data: Dict[str, Any]) -> Dict[str, Any]:
    """Example function to aggregate sales data"""
    events = window_data["events"]
    
    total_sales = sum(event.get("amount", 0) for event in events)
    avg_sales = total_sales / len(events) if events else 0
    max_sales = max((event.get("amount", 0) for event in events), default=0)
    
    return {
        "window_id": window_data["window_id"],
        "total_sales": total_sales,
        "average_sales": avg_sales,
        "max_sales": max_sales,
        "event_count": len(events),
        "processing_time": time.time()
    }

def detect_anomalies(window_data: Dict[str, Any]) -> Dict[str, Any]:
    """Example function to detect anomalies"""
    events = window_data["events"]
    
    if not events:
        return {"anomalies": [], "count": 0}
    
    # Simple anomaly detection based on value distribution
    values = [event.get("value", 0) for event in events]
    if len(values) < 2:
        return {"anomalies": [], "count": 0}
    
    mean_val = statistics.mean(values)
    std_val = statistics.stdev(values)
    
    anomalies = []
    for i, value in enumerate(values):
        if abs(value - mean_val) > 2 * std_val:  # 2 standard deviations
            anomalies.append({
                "index": i,
                "value": value,
                "z_score": abs(value - mean_val) / std_val if std_val > 0 else 0
            })
    
    return {
        "window_id": window_data["window_id"],
        "anomalies": anomalies,
        "anomaly_count": len(anomalies),
        "total_events": len(events),
        "processing_time": time.time()
    }

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_source", "create_processor", "create_sink", 
                     "start_processing", "stop_processing", "ingest_event", 
                     "get_stats", "get_sessions"
            - source_data: Stream source configuration
            - processor_data: Stream processor configuration
            - sink_data: Stream sink configuration
            - processing_data: Processing parameters
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_source":
            source_data = payload.get("source_data", {})
            
            source_id = _stream_engine.create_stream_source(
                name=source_data.get("name", "Stream Source"),
                stream_type=StreamType(source_data.get("stream_type", "kafka")),
                connection_config=source_data.get("connection_config", {}),
                topic=source_data.get("topic", "default"),
                partition=source_data.get("partition"),
                offset=source_data.get("offset")
            )
            
            return {
                "result": {
                    "source_id": source_id,
                    "message": f"Created stream source: {source_id}"
                },
                "metadata": {
                    "action": "create_source",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_processor":
            processor_data = payload.get("processor_data", {})
            
            # Get processing function
            func_name = processor_data.get("function", "aggregate_sales")
            if func_name == "aggregate_sales":
                processing_func = aggregate_sales_data
            elif func_name == "detect_anomalies":
                processing_func = detect_anomalies
            else:
                processing_func = lambda x: {"processed": True, "data": x}
            
            processor_id = _stream_engine.create_stream_processor(
                name=processor_data.get("name", "Stream Processor"),
                processing_mode=ProcessingMode(processor_data.get("processing_mode", "at_least_once")),
                window_type=WindowType(processor_data.get("window_type", "tumbling")),
                window_size=processor_data.get("window_size", 60000),  # 1 minute
                processing_function=processing_func,
                slide_interval=processor_data.get("slide_interval")
            )
            
            return {
                "result": {
                    "processor_id": processor_id,
                    "message": f"Created stream processor: {processor_id}"
                },
                "metadata": {
                    "action": "create_processor",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_sink":
            sink_data = payload.get("sink_data", {})
            
            sink_id = _stream_engine.create_stream_sink(
                name=sink_data.get("name", "Stream Sink"),
                stream_type=StreamType(sink_data.get("stream_type", "kafka")),
                connection_config=sink_data.get("connection_config", {}),
                topic=sink_data.get("topic", "output")
            )
            
            return {
                "result": {
                    "sink_id": sink_id,
                    "message": f"Created stream sink: {sink_id}"
                },
                "metadata": {
                    "action": "create_sink",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "start_processing":
            processing_data = payload.get("processing_data", {})
            
            session_id = await _stream_engine.start_stream_processing(
                source_id=processing_data.get("source_id", ""),
                processor_id=processing_data.get("processor_id", ""),
                sink_id=processing_data.get("sink_id")
            )
            
            return {
                "result": {
                    "session_id": session_id,
                    "message": f"Started stream processing: {session_id}"
                },
                "metadata": {
                    "action": "start_processing",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "stop_processing":
            session_id = payload.get("session_id", "")
            await _stream_engine.stop_stream_processing(session_id)
            
            return {
                "result": {
                    "session_id": session_id,
                    "message": f"Stopped stream processing: {session_id}"
                },
                "metadata": {
                    "action": "stop_processing",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "ingest_event":
            event_data = payload.get("event_data", {})
            
            event_id = await _stream_engine.ingest_event(
                source_id=event_data.get("source_id", ""),
                data=event_data.get("data", {})
            )
            
            return {
                "result": {
                    "event_id": event_id,
                    "message": f"Ingested event: {event_id}"
                },
                "metadata": {
                    "action": "ingest_event",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_stats":
            stats = _stream_engine.get_processing_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_sessions":
            sessions = _stream_engine.get_active_sessions()
            
            return {
                "result": sessions,
                "metadata": {
                    "action": "get_sessions",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        else:
            return {
                "result": {
                    "error": f"Unknown action: {action}"
                },
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    except Exception as e:
        logger.error(f"Error in stream_processing_engine: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
        }

# Example usage function
async def example_usage():
    """Example of how to use the stream processing engine skill"""
    
    # Create stream source
    source_id = await invoke({
        "action": "create_source",
        "source_data": {
            "name": "Sales Events",
            "stream_type": "kafka",
            "connection_config": {
                "bootstrap_servers": "localhost:9092",
                "group_id": "sales_processor"
            },
            "topic": "sales_events"
        }
    })
    
    print(f"Created source: {source_id['result']['source_id']}")
    
    # Create stream processor
    processor_id = await invoke({
        "action": "create_processor",
        "processor_data": {
            "name": "Sales Aggregator",
            "processing_mode": "at_least_once",
            "window_type": "tumbling",
            "window_size": 30000,  # 30 seconds
            "function": "aggregate_sales"
        }
    })
    
    print(f"Created processor: {processor_id['result']['processor_id']}")
    
    # Create stream sink
    sink_id = await invoke({
        "action": "create_sink",
        "sink_data": {
            "name": "Aggregated Sales",
            "stream_type": "kafka",
            "connection_config": {
                "bootstrap_servers": "localhost:9092"
            },
            "topic": "aggregated_sales"
        }
    })
    
    print(f"Created sink: {sink_id['result']['sink_id']}")
    
    # Start processing
    session_id = await invoke({
        "action": "start_processing",
        "processing_data": {
            "source_id": source_id['result']['source_id'],
            "processor_id": processor_id['result']['processor_id'],
            "sink_id": sink_id['result']['sink_id']
        }
    })
    
    print(f"Started processing: {session_id['result']['session_id']}")
    
    # Ingest some events
    for i in range(10):
        event_id = await invoke({
            "action": "ingest_event",
            "event_data": {
                "source_id": source_id['result']['source_id'],
                "data": {
                    "transaction_id": f"txn_{i}",
                    "amount": 100 + i * 10,
                    "product": f"product_{i % 3}",
                    "timestamp": time.time()
                }
            }
        })
        print(f"Ingested event: {event_id['result']['event_id']}")
        await asyncio.sleep(0.1)
    
    # Get processing statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Processing stats: {stats['result']}")
    
    # Stop processing
    await invoke({
        "action": "stop_processing",
        "session_id": session_id['result']['session_id']
    })
    
    print("Stopped processing")

if __name__ == "__main__":
    asyncio.run(example_usage())