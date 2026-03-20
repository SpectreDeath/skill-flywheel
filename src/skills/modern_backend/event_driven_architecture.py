#!/usr/bin/env python3
"""
Skill: event-driven-architecture
Domain: modern_backend
Description: Event-driven architecture and message queuing system
"""

import asyncio
import logging
import random
import time
import uuid
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Event types"""
    COMMAND = "command"
    EVENT = "event"
    QUERY = "query"
    INTEGRATION = "integration"

class EventStatus(Enum):
    """Event processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

class QueueType(Enum):
    """Queue types"""
    FIFO = "fifo"
    PRIORITY = "priority"
    DEAD_LETTER = "dead_letter"

class SubscriptionType(Enum):
    """Subscription types"""
    PUSH = "push"
    PULL = "pull"
    WEBSOCKET = "websocket"

@dataclass
class Event:
    """Represents an event"""
    event_id: str
    event_type: EventType
    event_name: str
    payload: Dict[str, Any]
    source: str
    timestamp: float
    correlation_id: str | None
    causation_id: str | None
    metadata: Dict[str, Any]
    retries: int
    max_retries: int
    status: EventStatus

@dataclass
class Queue:
    """Represents a message queue"""
    queue_id: str
    name: str
    queue_type: QueueType
    max_size: int
    ttl: int  # Time to live in seconds
    messages: deque
    consumers: List[str]
    created_at: float

@dataclass
class Consumer:
    """Represents a message consumer"""
    consumer_id: str
    name: str
    queue_id: str
    subscription_type: SubscriptionType
    callback_url: str | None
    batch_size: int
    concurrency: int
    retry_policy: Dict[str, Any]
    created_at: float

@dataclass
class Topic:
    """Represents a message topic"""
    topic_id: str
    name: str
    partitions: int
    replication_factor: int
    retention_days: int
    subscriptions: List[str]
    created_at: float

@dataclass
class Subscription:
    """Represents a topic subscription"""
    subscription_id: str
    topic_id: str
    consumer_id: str
    filter_rules: Dict[str, Any]
    created_at: float

@dataclass
class EventStore:
    """Represents an event store"""
    store_id: str
    name: str
    events: List[Event]
    max_events: int
    retention_days: int
    created_at: float

class EventDrivenArchitecture:
    """Event-driven architecture and message queuing system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the event-driven architecture system
        
        Args:
            config: Configuration dictionary with:
                - max_queue_size: Maximum queue size
                - default_ttl: Default time to live for messages
                - max_retries: Maximum retry attempts
                - retry_delay: Delay between retries
        """
        self.max_queue_size = config.get("max_queue_size", 10000)
        self.default_ttl = config.get("default_ttl", 3600)
        self.max_retries = config.get("max_retries", 3)
        self.retry_delay = config.get("retry_delay", 5)
        
        self.queues: Dict[str, Queue] = {}
        self.consumers: Dict[str, Consumer] = {}
        self.topics: Dict[str, Topic] = {}
        self.subscriptions: Dict[str, Subscription] = {}
        self.event_stores: Dict[str, EventStore] = {}
        
        self.event_processing_stats = {
            "total_events": 0,
            "processed_events": 0,
            "failed_events": 0,
            "average_processing_time": 0.0,
            "queue_depth": 0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background services
        self._event_processor_task = asyncio.create_task(self._event_processor_loop())
        self._queue_monitor_task = asyncio.create_task(self._queue_monitor_loop())
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    def create_queue(self,
                    name: str,
                    queue_type: QueueType = QueueType.FIFO,
                    max_size: int = 1000,
                    ttl: int = 3600) -> str:
        """
        Create a message queue
        
        Args:
            name: Queue name
            queue_type: Type of queue
            max_size: Maximum queue size
            ttl: Time to live for messages
            
        Returns:
            Queue ID
        """
        queue_id = str(uuid.uuid4())
        
        queue = Queue(
            queue_id=queue_id,
            name=name,
            queue_type=queue_type,
            max_size=max_size,
            ttl=ttl,
            messages=deque(maxlen=max_size),
            consumers=[],
            created_at=time.time()
        )
        
        self.queues[queue_id] = queue
        self.logger.info(f"Created queue: {queue_id} ({name})")
        return queue_id
    
    def create_consumer(self,
                       name: str,
                       queue_id: str,
                       subscription_type: SubscriptionType = SubscriptionType.PULL,
                       callback_url: str | None = None,
                       batch_size: int = 1,
                       concurrency: int = 1,
                       retry_policy: Dict[str, Any] | None = None) -> str:
        """
        Create a message consumer
        
        Args:
            name: Consumer name
            queue_id: Queue ID to consume from
            subscription_type: Type of subscription
            callback_url: Callback URL for push subscriptions
            batch_size: Number of messages to process in batch
            concurrency: Number of concurrent consumers
            retry_policy: Retry policy configuration
            
        Returns:
            Consumer ID
        """
        consumer_id = str(uuid.uuid4())
        
        consumer = Consumer(
            consumer_id=consumer_id,
            name=name,
            queue_id=queue_id,
            subscription_type=subscription_type,
            callback_url=callback_url,
            batch_size=batch_size,
            concurrency=concurrency,
            retry_policy=retry_policy or {"max_retries": 3, "backoff_factor": 2.0},
            created_at=time.time()
        )
        
        self.consumers[consumer_id] = consumer
        
        # Add consumer to queue
        if queue_id in self.queues:
            self.queues[queue_id].consumers.append(consumer_id)
        
        self.logger.info(f"Created consumer: {consumer_id} ({name})")
        return consumer_id
    
    def create_topic(self,
                    name: str,
                    partitions: int = 1,
                    replication_factor: int = 1,
                    retention_days: int = 7) -> str:
        """
        Create a message topic
        
        Args:
            name: Topic name
            partitions: Number of partitions
            replication_factor: Replication factor
            retention_days: Retention period in days
            
        Returns:
            Topic ID
        """
        topic_id = str(uuid.uuid4())
        
        topic = Topic(
            topic_id=topic_id,
            name=name,
            partitions=partitions,
            replication_factor=replication_factor,
            retention_days=retention_days,
            subscriptions=[],
            created_at=time.time()
        )
        
        self.topics[topic_id] = topic
        self.logger.info(f"Created topic: {topic_id} ({name})")
        return topic_id
    
    def create_subscription(self,
                           topic_id: str,
                           consumer_id: str,
                           filter_rules: Dict[str, Any] | None = None) -> str:
        """
        Create a topic subscription
        
        Args:
            topic_id: Topic ID
            consumer_id: Consumer ID
            filter_rules: Filter rules for subscription
            
        Returns:
            Subscription ID
        """
        subscription_id = str(uuid.uuid4())
        
        subscription = Subscription(
            subscription_id=subscription_id,
            topic_id=topic_id,
            consumer_id=consumer_id,
            filter_rules=filter_rules or {},
            created_at=time.time()
        )
        
        self.subscriptions[subscription_id] = subscription
        
        # Add subscription to topic
        if topic_id in self.topics:
            self.topics[topic_id].subscriptions.append(subscription_id)
        
        self.logger.info(f"Created subscription: {subscription_id}")
        return subscription_id
    
    def create_event_store(self,
                          name: str,
                          max_events: int = 100000,
                          retention_days: int = 30) -> str:
        """
        Create an event store
        
        Args:
            name: Event store name
            max_events: Maximum number of events to store
            retention_days: Retention period in days
            
        Returns:
            Event store ID
        """
        store_id = str(uuid.uuid4())
        
        event_store = EventStore(
            store_id=store_id,
            name=name,
            events=[],
            max_events=max_events,
            retention_days=retention_days,
            created_at=time.time()
        )
        
        self.event_stores[store_id] = event_store
        self.logger.info(f"Created event store: {store_id} ({name})")
        return store_id
    
    def publish_event(self,
                     event_name: str,
                     payload: Dict[str, Any],
                     event_type: EventType = EventType.EVENT,
                     source: str = "system",
                     correlation_id: str | None = None,
                     causation_id: str | None = None,
                     metadata: Dict[str, Any] | None = None) -> str:
        """
        Publish an event to the system
        
        Args:
            event_name: Name of the event
            payload: Event payload
            event_type: Type of event
            source: Source of the event
            correlation_id: Correlation ID for tracing
            causation_id: Causation ID for event sourcing
            metadata: Additional metadata
            
        Returns:
            Event ID
        """
        event_id = str(uuid.uuid4())
        
        event = Event(
            event_id=event_id,
            event_type=event_type,
            event_name=event_name,
            payload=payload,
            source=source,
            timestamp=time.time(),
            correlation_id=correlation_id,
            causation_id=causation_id,
            metadata=metadata or {},
            retries=0,
            max_retries=self.max_retries,
            status=EventStatus.PENDING
        )
        
        # Store in event store
        for _store_id, store in self.event_stores.items():
            store.events.append(event)
            if len(store.events) > store.max_events:
                store.events.pop(0)
        
        # Route to appropriate queues/topics
        self._route_event(event)
        
        self.event_processing_stats["total_events"] += 1
        self.logger.info(f"Published event: {event_id} ({event_name})")
        return event_id
    
    def enqueue_message(self,
                       queue_id: str,
                       message: Dict[str, Any],
                       priority: int = 0) -> bool:
        """
        Enqueue a message to a queue
        
        Args:
            queue_id: Queue ID
            message: Message to enqueue
            priority: Message priority (for priority queues)
            
        Returns:
            Success status
        """
        if queue_id not in self.queues:
            return False
        
        queue = self.queues[queue_id]
        
        # Check queue size
        if len(queue.messages) >= queue.max_size:
            self.logger.warning(f"Queue {queue_id} is full")
            return False
        
        # Create message with metadata
        message_data = {
            "id": str(uuid.uuid4()),
            "payload": message,
            "priority": priority,
            "timestamp": time.time(),
            "ttl": queue.ttl
        }
        
        # Add to queue based on type
        if queue.queue_type == QueueType.FIFO:
            queue.messages.append(message_data)
        elif queue.queue_type == QueueType.PRIORITY:
            # Insert in priority order (higher priority first)
            inserted = False
            for i, msg in enumerate(queue.messages):
                if msg["priority"] < priority:
                    queue.messages.insert(i, message_data)
                    inserted = True
                    break
            if not inserted:
                queue.messages.append(message_data)
        else:
            queue.messages.append(message_data)
        
        self.event_processing_stats["queue_depth"] += 1
        self.logger.info(f"Enqueued message to {queue_id}")
        return True
    
    def dequeue_message(self, queue_id: str) -> Dict[str, Any] | None:
        """
        Dequeue a message from a queue
        
        Args:
            queue_id: Queue ID
            
        Returns:
            Message data or None
        """
        if queue_id not in self.queues:
            return None
        
        queue = self.queues[queue_id]
        
        if not queue.messages:
            return None
        
        # Get message based on queue type
        if queue.queue_type in (QueueType.FIFO, QueueType.PRIORITY):
            message = queue.messages.popleft()
        else:
            message = queue.messages.popleft()
        
        self.event_processing_stats["queue_depth"] -= 1
        return message
    
    def get_event_stats(self) -> Dict[str, Any]:
        """Get event processing statistics"""
        return {
            "total_events": self.event_processing_stats["total_events"],
            "processed_events": self.event_processing_stats["processed_events"],
            "failed_events": self.event_processing_stats["failed_events"],
            "average_processing_time": self.event_processing_stats["average_processing_time"],
            "queue_depth": self.event_processing_stats["queue_depth"],
            "total_queues": len(self.queues),
            "total_consumers": len(self.consumers),
            "total_topics": len(self.topics),
            "total_subscriptions": len(self.subscriptions),
            "total_event_stores": len(self.event_stores)
        }
    
    def get_queue_stats(self, queue_id: str) -> Dict[str, Any]:
        """Get queue statistics"""
        if queue_id not in self.queues:
            return {}
        
        queue = self.queues[queue_id]
        
        return {
            "queue_id": queue_id,
            "name": queue.name,
            "type": queue.queue_type.value,
            "current_size": len(queue.messages),
            "max_size": queue.max_size,
            "consumer_count": len(queue.consumers),
            "ttl": queue.ttl
        }
    
    def _route_event(self, event: Event):
        """Route event to appropriate queues/topics"""
        # In a real implementation, this would use routing rules
        # For now, route to all queues that match the event name pattern
        
        for queue_id, queue in self.queues.items():
            # Simple routing based on event name prefix
            if event.event_name.startswith(queue.name):
                self.enqueue_message(queue_id, {
                    "event_id": event.event_id,
                    "event_name": event.event_name,
                    "payload": event.payload,
                    "source": event.source,
                    "timestamp": event.timestamp
                })
    
    def _process_event(self, event: Event) -> bool:
        """Process an event"""
        start_time = time.time()
        
        try:
            # Find consumers for this event
            consumers = self._find_consumers_for_event(event)
            
            if not consumers:
                self.logger.warning(f"No consumers found for event: {event.event_name}")
                return True
            
            # Process event with each consumer
            for consumer_id in consumers:
                consumer = self.consumers[consumer_id]
                
                try:
                    if consumer.subscription_type == SubscriptionType.PUSH:
                        # Send to callback URL
                        self._send_to_callback(consumer, event)
                    elif consumer.subscription_type == SubscriptionType.PULL:
                        # Enqueue to consumer's queue
                        queue_id = consumer.queue_id
                        self.enqueue_message(queue_id, {
                            "event_id": event.event_id,
                            "event_name": event.event_name,
                            "payload": event.payload,
                            "source": event.source,
                            "timestamp": event.timestamp
                        })
                    elif consumer.subscription_type == SubscriptionType.WEBSOCKET:
                        # Send via WebSocket (simulated)
                        self._send_via_websocket(consumer, event)
                
                except Exception as e:
                    self.logger.error(f"Error processing event {event.event_id} with consumer {consumer_id}: {e}")
                    event.retries += 1
                    
                    if event.retries >= event.max_retries:
                        event.status = EventStatus.FAILED
                        self.event_processing_stats["failed_events"] += 1
                        return False
            
            event.status = EventStatus.COMPLETED
            self.event_processing_stats["processed_events"] += 1
            
            # Update average processing time
            total_time = self.event_processing_stats["average_processing_time"] * (self.event_processing_stats["processed_events"] - 1)
            self.event_processing_stats["average_processing_time"] = (total_time + (time.time() - start_time)) / self.event_processing_stats["processed_events"]
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing event {event.event_id}: {e}")
            return False
    
    def _find_consumers_for_event(self, event: Event) -> List[str]:
        """Find consumers for an event"""
        consumers = []
        
        # Find topics that match the event
        for _topic_id, topic in self.topics.items():
            if event.event_name.startswith(topic.name):
                # Find subscriptions for this topic
                for subscription_id in topic.subscriptions:
                    subscription = self.subscriptions[subscription_id]
                    consumers.append(subscription.consumer_id)
        
        return consumers
    
    def _send_to_callback(self, consumer: Consumer, event: Event):
        """Send event to callback URL"""
        # In a real implementation, this would make HTTP requests
        # For now, simulate the callback
        
        # Simulate network delay and potential failures
        random.uniform(0.1, 1.0)
        success = random.choices([True, False], weights=[90, 10])[0]
        
        if not success:
            raise Exception(f"Callback failed for consumer {consumer.name}")
    
    def _send_via_websocket(self, consumer: Consumer, event: Event):
        """Send event via WebSocket"""
        # In a real implementation, this would use WebSocket connections
        # For now, simulate the WebSocket message
        self.logger.info(f"Sent event {event.event_name} via WebSocket to {consumer.name}")
    
    async def _event_processor_loop(self):
        """Background event processor loop"""
        while True:
            try:
                await self._process_pending_events()
                await asyncio.sleep(1)
            except Exception as e:
                self.logger.error(f"Error in event processor loop: {e}")
                await asyncio.sleep(1)
    
    async def _process_pending_events(self):
        """Process pending events"""
        # Process events from queues
        for queue_id, queue in self.queues.items():
            if queue.messages:
                message = self.dequeue_message(queue_id)
                if message:
                    # Simulate processing
                    await asyncio.sleep(0.1)
                    self.logger.info(f"Processed message from queue {queue_id}")
    
    async def _queue_monitor_loop(self):
        """Background queue monitor loop"""
        while True:
            try:
                await self._monitor_queues()
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Error in queue monitor loop: {e}")
                await asyncio.sleep(30)
    
    async def _monitor_queues(self):
        """Monitor queue health and performance"""
        for queue_id, queue in self.queues.items():
            # Check for stuck messages
            current_time = time.time()
            stuck_messages = [
                msg for msg in queue.messages
                if current_time - msg["timestamp"] > msg["ttl"]
            ]
            
            for msg in stuck_messages:
                self.logger.warning(f"Message {msg['id']} stuck in queue {queue_id}")
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                await self._cleanup_expired_data()
                await asyncio.sleep(3600)  # Run every hour
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(3600)
    
    async def _cleanup_expired_data(self):
        """Clean up expired messages and events"""
        current_time = time.time()
        current_time - (24 * 3600)  # 24 hours ago
        
        # Clean up expired messages from queues
        for _queue_id, queue in self.queues.items():
            queue.messages = deque([
                msg for msg in queue.messages
                if current_time - msg["timestamp"] <= msg["ttl"]
            ])
        
        # Clean up old events from stores
        for _store_id, store in self.event_stores.items():
            store.events = [
                event for event in store.events
                if current_time - event.timestamp <= (store.retention_days * 24 * 3600)
            ]

# Global event-driven architecture instance
_event_system = EventDrivenArchitecture({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_queue", "create_consumer", "create_topic", 
                     "create_subscription", "create_store", "publish_event", 
                     "enqueue_message", "dequeue_message", "get_stats", "get_queue_stats"
            - queue_data: Queue configuration
            - consumer_data: Consumer configuration
            - topic_data: Topic configuration
            - subscription_data: Subscription configuration
            - store_data: Event store configuration
            - event_data: Event data
            - message_data: Message data
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_queue":
            queue_data = payload.get("queue_data", {})
            
            queue_id = _event_system.create_queue(
                name=queue_data.get("name", "Queue"),
                queue_type=QueueType(queue_data.get("queue_type", "fifo")),
                max_size=queue_data.get("max_size", 1000),
                ttl=queue_data.get("ttl", 3600)
            )
            
            return {
                "result": {
                    "queue_id": queue_id,
                    "message": f"Created queue: {queue_id}"
                },
                "metadata": {
                    "action": "create_queue",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_consumer":
            consumer_data = payload.get("consumer_data", {})
            
            consumer_id = _event_system.create_consumer(
                name=consumer_data.get("name", "Consumer"),
                queue_id=consumer_data.get("queue_id", ""),
                subscription_type=SubscriptionType(consumer_data.get("subscription_type", "pull")),
                callback_url=consumer_data.get("callback_url"),
                batch_size=consumer_data.get("batch_size", 1),
                concurrency=consumer_data.get("concurrency", 1),
                retry_policy=consumer_data.get("retry_policy")
            )
            
            return {
                "result": {
                    "consumer_id": consumer_id,
                    "message": f"Created consumer: {consumer_id}"
                },
                "metadata": {
                    "action": "create_consumer",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_topic":
            topic_data = payload.get("topic_data", {})
            
            topic_id = _event_system.create_topic(
                name=topic_data.get("name", "Topic"),
                partitions=topic_data.get("partitions", 1),
                replication_factor=topic_data.get("replication_factor", 1),
                retention_days=topic_data.get("retention_days", 7)
            )
            
            return {
                "result": {
                    "topic_id": topic_id,
                    "message": f"Created topic: {topic_id}"
                },
                "metadata": {
                    "action": "create_topic",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_subscription":
            subscription_data = payload.get("subscription_data", {})
            
            subscription_id = _event_system.create_subscription(
                topic_id=subscription_data.get("topic_id", ""),
                consumer_id=subscription_data.get("consumer_id", ""),
                filter_rules=subscription_data.get("filter_rules")
            )
            
            return {
                "result": {
                    "subscription_id": subscription_id,
                    "message": f"Created subscription: {subscription_id}"
                },
                "metadata": {
                    "action": "create_subscription",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_store":
            store_data = payload.get("store_data", {})
            
            store_id = _event_system.create_event_store(
                name=store_data.get("name", "Event Store"),
                max_events=store_data.get("max_events", 100000),
                retention_days=store_data.get("retention_days", 30)
            )
            
            return {
                "result": {
                    "store_id": store_id,
                    "message": f"Created event store: {store_id}"
                },
                "metadata": {
                    "action": "create_store",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "publish_event":
            event_data = payload.get("event_data", {})
            
            event_id = _event_system.publish_event(
                event_name=event_data.get("event_name", "Event"),
                payload=event_data.get("payload", {}),
                event_type=EventType(event_data.get("event_type", "event")),
                source=event_data.get("source", "system"),
                correlation_id=event_data.get("correlation_id"),
                causation_id=event_data.get("causation_id"),
                metadata=event_data.get("metadata")
            )
            
            return {
                "result": {
                    "event_id": event_id,
                    "message": f"Published event: {event_id}"
                },
                "metadata": {
                    "action": "publish_event",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "enqueue_message":
            message_data = payload.get("message_data", {})
            
            success = _event_system.enqueue_message(
                queue_id=message_data.get("queue_id", ""),
                message=message_data.get("message", {}),
                priority=message_data.get("priority", 0)
            )
            
            return {
                "result": {
                    "success": success,
                    "message": "Message enqueued" if success else "Failed to enqueue message"
                },
                "metadata": {
                    "action": "enqueue_message",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "dequeue_message":
            queue_id = payload.get("queue_id", "")
            message = _event_system.dequeue_message(queue_id)
            
            return {
                "result": message,
                "metadata": {
                    "action": "dequeue_message",
                    "timestamp": datetime.now().isoformat(),
                    "queue_id": queue_id
                }
            }
        
        elif action == "get_stats":
            stats = _event_system.get_event_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_queue_stats":
            queue_id = payload.get("queue_id", "")
            stats = _event_system.get_queue_stats(queue_id)
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_queue_stats",
                    "timestamp": datetime.now().isoformat(),
                    "queue_id": queue_id
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
        logger.error(f"Error in event_driven_architecture: {e}")
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
    """Example of how to use the event-driven architecture skill"""
    
    # Create queues
    user_queue = await invoke({
        "action": "create_queue",
        "queue_data": {
            "name": "user-events",
            "queue_type": "fifo",
            "max_size": 1000,
            "ttl": 3600
        }
    })
    
    order_queue = await invoke({
        "action": "create_queue",
        "queue_data": {
            "name": "order-events",
            "queue_type": "priority",
            "max_size": 2000,
            "ttl": 7200
        }
    })
    
    print(f"Created queues: {user_queue['result']['queue_id']}, {order_queue['result']['queue_id']}")
    
    # Create consumers
    user_consumer = await invoke({
        "action": "create_consumer",
        "consumer_data": {
            "name": "User Event Consumer",
            "queue_id": user_queue['result']['queue_id'],
            "subscription_type": "pull",
            "batch_size": 10,
            "concurrency": 2,
            "retry_policy": {"max_retries": 3, "backoff_factor": 2.0}
        }
    })
    
    order_consumer = await invoke({
        "action": "create_consumer",
        "consumer_data": {
            "name": "Order Event Consumer",
            "queue_id": order_queue['result']['queue_id'],
            "subscription_type": "push",
            "callback_url": "http://localhost:3000/webhook",
            "batch_size": 5,
            "concurrency": 1,
            "retry_policy": {"max_retries": 5, "backoff_factor": 1.5}
        }
    })
    
    print(f"Created consumers: {user_consumer['result']['consumer_id']}, {order_consumer['result']['consumer_id']}")
    
    # Create topics
    user_topic = await invoke({
        "action": "create_topic",
        "topic_data": {
            "name": "user-events",
            "partitions": 3,
            "replication_factor": 2,
            "retention_days": 7
        }
    })
    
    order_topic = await invoke({
        "action": "create_topic",
        "topic_data": {
            "name": "order-events",
            "partitions": 2,
            "replication_factor": 2,
            "retention_days": 14
        }
    })
    
    print(f"Created topics: {user_topic['result']['topic_id']}, {order_topic['result']['topic_id']}")
    
    # Create subscriptions
    user_subscription = await invoke({
        "action": "create_subscription",
        "subscription_data": {
            "topic_id": user_topic['result']['topic_id'],
            "consumer_id": user_consumer['result']['consumer_id'],
            "filter_rules": {"event_type": "user"}
        }
    })
    
    order_subscription = await invoke({
        "action": "create_subscription",
        "subscription_data": {
            "topic_id": order_topic['result']['topic_id'],
            "consumer_id": order_consumer['result']['consumer_id'],
            "filter_rules": {"event_type": "order"}
        }
    })
    
    print(f"Created subscriptions: {user_subscription['result']['subscription_id']}, {order_subscription['result']['subscription_id']}")
    
    # Create event store
    event_store = await invoke({
        "action": "create_store",
        "store_data": {
            "name": "System Events",
            "max_events": 50000,
            "retention_days": 30
        }
    })
    
    print(f"Created event store: {event_store['result']['store_id']}")
    
    # Publish events
    user_created_event = await invoke({
        "action": "publish_event",
        "event_data": {
            "event_name": "user.created",
            "payload": {
                "user_id": "user123",
                "email": "user@example.com",
                "name": "John Doe"
            },
            "event_type": "event",
            "source": "user-service",
            "correlation_id": "corr-123",
            "metadata": {"version": "1.0"}
        }
    })
    
    order_placed_event = await invoke({
        "action": "publish_event",
        "event_data": {
            "event_name": "order.placed",
            "payload": {
                "order_id": "order456",
                "user_id": "user123",
                "amount": 99.99,
                "items": ["item1", "item2"]
            },
            "event_type": "event",
            "source": "order-service",
            "correlation_id": "corr-456",
            "metadata": {"version": "1.0"}
        }
    })
    
    print(f"Published events: {user_created_event['result']['event_id']}, {order_placed_event['result']['event_id']}")
    
    # Enqueue messages
    await invoke({
        "action": "enqueue_message",
        "message_data": {
            "queue_id": user_queue['result']['queue_id'],
            "message": {
                "type": "user_notification",
                "user_id": "user123",
                "message": "Welcome to our platform!"
            },
            "priority": 5
        }
    })
    
    await invoke({
        "action": "enqueue_message",
        "message_data": {
            "queue_id": order_queue['result']['queue_id'],
            "message": {
                "type": "order_confirmation",
                "order_id": "order456",
                "status": "confirmed"
            },
            "priority": 10
        }
    })
    
    # Dequeue messages
    user_message = await invoke({
        "action": "dequeue_message",
        "queue_id": user_queue['result']['queue_id']
    })
    
    order_message = await invoke({
        "action": "dequeue_message",
        "queue_id": order_queue['result']['queue_id']
    })
    
    print(f"Dequeued messages: {user_message['result']}, {order_message['result']}")
    
    # Get statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Event system stats: {stats['result']}")
    
    user_queue_stats = await invoke({
        "action": "get_queue_stats",
        "queue_id": user_queue['result']['queue_id']
    })
    
    print(f"User queue stats: {user_queue_stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
