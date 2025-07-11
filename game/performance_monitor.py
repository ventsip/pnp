"""
Performance monitoring utilities for the complexity theory game
"""

import time
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class PerformanceMetric:
    """Individual performance metric"""
    name: str
    value: float
    timestamp: float
    category: str

class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, List[PerformanceMetric]] = defaultdict(list)
        self.timers: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.enabled = True
    
    def start_timer(self, name: str):
        """Start a performance timer"""
        if not self.enabled:
            return
        
        with self.lock:
            self.timers[name] = time.time()
    
    def end_timer(self, name: str, category: str = "general") -> Optional[float]:
        """End a performance timer and record the metric"""
        if not self.enabled:
            return None
        
        with self.lock:
            if name not in self.timers:
                return None
            
            duration = time.time() - self.timers[name]
            del self.timers[name]
            
            metric = PerformanceMetric(
                name=name,
                value=duration,
                timestamp=time.time(),
                category=category
            )
            
            self.metrics[name].append(metric)
            return duration
    
    def record_metric(self, name: str, value: float, category: str = "general"):
        """Record a custom metric"""
        if not self.enabled:
            return
        
        with self.lock:
            metric = PerformanceMetric(
                name=name,
                value=value,
                timestamp=time.time(),
                category=category
            )
            
            self.metrics[name].append(metric)
    
    def get_average(self, name: str, last_n: Optional[int] = None) -> float:
        """Get average value for a metric"""
        with self.lock:
            if name not in self.metrics:
                return 0.0
            
            metrics = self.metrics[name]
            if last_n:
                metrics = metrics[-last_n:]
            
            if not metrics:
                return 0.0
            
            return sum(m.value for m in metrics) / len(metrics)
    
    def get_summary(self) -> Dict[str, Dict[str, float]]:
        """Get performance summary"""
        with self.lock:
            summary = {}
            
            for name, metrics in self.metrics.items():
                if not metrics:
                    continue
                
                values = [m.value for m in metrics]
                summary[name] = {
                    'count': len(values),
                    'average': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'total': sum(values)
                }
            
            return summary
    
    def clear_metrics(self):
        """Clear all recorded metrics"""
        with self.lock:
            self.metrics.clear()
            self.timers.clear()
    
    def disable(self):
        """Disable performance monitoring"""
        self.enabled = False
    
    def enable(self):
        """Enable performance monitoring"""
        self.enabled = True
    
    def print_summary(self):
        """Print performance summary to console"""
        summary = self.get_summary()
        
        if not summary:
            print("No performance metrics recorded.")
            return
        
        print("\n" + "="*60)
        print("PERFORMANCE SUMMARY")
        print("="*60)
        
        for name, stats in summary.items():
            print(f"\n{name}:")
            print(f"  Count: {stats['count']}")
            print(f"  Average: {stats['average']:.3f}s")
            print(f"  Min: {stats['min']:.3f}s")
            print(f"  Max: {stats['max']:.3f}s")
            print(f"  Total: {stats['total']:.3f}s")
        
        print("\n" + "="*60)

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

class PerformanceContext:
    """Context manager for performance timing"""
    
    def __init__(self, name: str, category: str = "general", monitor: PerformanceMonitor = None):
        self.name = name
        self.category = category
        self.monitor = monitor or performance_monitor
    
    def __enter__(self):
        self.monitor.start_timer(self.name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.monitor.end_timer(self.name, self.category)

def time_it(category: str = "general", monitor: PerformanceMonitor = None):
    """Decorator for timing function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with PerformanceContext(func.__name__, category, monitor):
                return func(*args, **kwargs)
        return wrapper
    return decorator