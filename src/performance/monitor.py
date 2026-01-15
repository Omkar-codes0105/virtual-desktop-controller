"""Performance monitoring module."""
import logging
import time
from typing import Dict, Any, Optional
from collections import deque

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitors and tracks application performance metrics.
    
    Tracks FPS, latency, memory usage, and other performance indicators.
    Can be extended for specialized monitoring requirements.
    """
    
    def __init__(self, window_size: int = 60, config: Optional[Dict[str, Any]] = None):
        """Initialize performance monitor.
        
        Args:
            window_size: Number of frames to keep in rolling window for averaging
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.window_size = window_size
        
        # Performance metrics
        self.fps = 0.0
        self.latency_ms = 0.0
        self.memory_mb = 0.0
        
        # Rolling window for averaging
        self.frame_times = deque(maxlen=window_size)
        self.latencies = deque(maxlen=window_size)
        
        # Timestamps
        self.last_frame_time = time.time()
        self.is_initialized = False
        
        logger.info(f"PerformanceMonitor initialized with window_size={window_size}")
    
    def initialize(self) -> bool:
        """Initialize performance monitor.
        
        Returns:
            True if initialization successful
        """
        try:
            self.is_initialized = True
            self.last_frame_time = time.time()
            logger.info("PerformanceMonitor initialization complete")
            return True
        except Exception as e:
            logger.error(f"PerformanceMonitor initialization failed: {e}")
            return False
    
    def update(self, latency_ms: float = 0.0) -> None:
        """Update performance metrics.
        
        Args:
            latency_ms: Frame processing latency in milliseconds
        """
        if not self.is_initialized:
            return
        
        try:
            current_time = time.time()
            frame_time = (current_time - self.last_frame_time) * 1000  # Convert to ms
            self.last_frame_time = current_time
            
            # Store measurements
            self.frame_times.append(frame_time)
            self.latencies.append(latency_ms)
            
            # Calculate averages
            if self.frame_times:
                avg_frame_time = sum(self.frame_times) / len(self.frame_times)
                self.fps = 1000.0 / avg_frame_time if avg_frame_time > 0 else 0.0
            
            if self.latencies:
                self.latency_ms = sum(self.latencies) / len(self.latencies)
        
        except Exception as e:
            logger.error(f"Error updating performance metrics: {e}")
    
    def get_stats(self) -> Dict[str, float]:
        """Get current performance statistics.
        
        Returns:
            Dictionary with performance metrics
        """
        return {
            'fps': self.fps,
            'latency_ms': self.latency_ms,
            'memory_mb': self.memory_mb,
            'frame_count': len(self.frame_times)
        }
    
    def get_fps(self) -> float:
        """Get current FPS.
        
        Returns:
            Frames per second
        """
        return self.fps
    
    def get_latency(self) -> float:
        """Get average latency.
        
        Returns:
            Latency in milliseconds
        """
        return self.latency_ms
    
    def reset(self) -> None:
        """Reset all performance metrics."""
        self.frame_times.clear()
        self.latencies.clear()
        self.fps = 0.0
        self.latency_ms = 0.0
        self.last_frame_time = time.time()
        logger.info("Performance metrics reset")
    
    def log_stats(self) -> None:
        """Log current performance statistics."""
        stats = self.get_stats()
        logger.info(f"Performance - FPS: {stats['fps']:.2f}, "
                   f"Latency: {stats['latency_ms']:.2f}ms, "
                   f"Memory: {stats['memory_mb']:.2f}MB")
    
    def shutdown(self) -> None:
        """Shutdown the monitor and release resources."""
        self.is_initialized = False
        logger.info("PerformanceMonitor shutdown")
