from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, Any
import time

class AgentMetrics:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        
        # Request metrics
        self.request_counter = Counter(
            'agent_requests_total',
            'Total number of requests processed',
            ['agent_id', 'status']
        )
        
        # Latency metrics
        self.request_latency = Histogram(
            'agent_request_duration_seconds',
            'Request duration in seconds',
            ['agent_id', 'operation']
        )
        
        # System metrics
        self.memory_usage = Gauge(
            'agent_memory_usage_bytes',
            'Current memory usage in bytes',
            ['agent_id']
        )

    def track_request(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                self.request_counter.labels(
                    agent_id=self.agent_id,
                    status='success'
                ).inc()
                return result
            except Exception as e:
                self.request_counter.labels(
                    agent_id=self.agent_id,
                    status='error'
                ).inc()
                raise e
            finally:
                duration = time.time() - start_time
                self.request_latency.labels(
                    agent_id=self.agent_id,
                    operation=func.__name__
                ).observe(duration)
        return wrapper