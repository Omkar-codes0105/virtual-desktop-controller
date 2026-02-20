"""Kalman filter-based eye tracking smoother for gaze estimation."""
import logging
import numpy as np
from typing import Optional, Tuple

try:
    from filterpy.kalman import KalmanFilter
    HAS_FILTERPY = True
except ImportError:
    HAS_FILTERPY = False

logger = logging.getLogger(__name__)


class KalmanTracker:
    """Kalman filter for smoothing eye gaze tracking output.

    Reduces jitter and noise in iris/gaze position estimates.
    Falls back to simple moving average if filterpy is not available.
    """

    def __init__(self, process_noise: float = 1e-3, measurement_noise: float = 1e-1):
        """Initialize Kalman tracker.

        Args:
            process_noise: Process noise covariance (lower = smoother, higher = more responsive)
            measurement_noise: Measurement noise covariance
        """
        self._kf_x = None
        self._kf_y = None
        self._initialized = False
        self._fallback_window = []
        self._window_size = 5

        if HAS_FILTERPY:
            self._init_kalman_filters(process_noise, measurement_noise)
            logger.info("KalmanTracker initialized with filterpy")
        else:
            logger.warning("filterpy not available. Using moving average fallback.")

    def _init_kalman_filters(self, process_noise: float, measurement_noise: float):
        """Initialize two separate Kalman filters for x and y coordinates."""
        # X coordinate filter
        self._kf_x = KalmanFilter(dim_x=2, dim_z=1)
        self._kf_x.F = np.array([[1, 1], [0, 1]])  # State transition
        self._kf_x.H = np.array([[1, 0]])           # Measurement function
        self._kf_x.R *= measurement_noise            # Measurement noise
        self._kf_x.Q *= process_noise                # Process noise
        self._kf_x.P *= 1.0                         # Initial covariance

        # Y coordinate filter
        self._kf_y = KalmanFilter(dim_x=2, dim_z=1)
        self._kf_y.F = np.array([[1, 1], [0, 1]])
        self._kf_y.H = np.array([[1, 0]])
        self._kf_y.R *= measurement_noise
        self._kf_y.Q *= process_noise
        self._kf_y.P *= 1.0

    def update(self, gaze_point: Optional[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
        """Update the Kalman filter with a new gaze measurement.

        Args:
            gaze_point: Tuple (x, y) normalized 0-1, or None if no detection

        Returns:
            Smoothed gaze point (x, y) or None if not enough data
        """
        if gaze_point is None:
            return None

        x, y = gaze_point

        if HAS_FILTERPY and self._kf_x is not None:
            return self._kalman_update(x, y)
        else:
            return self._moving_average_update(x, y)

    def _kalman_update(self, x: float, y: float) -> Tuple[float, float]:
        """Update using Kalman filter."""
        if not self._initialized:
            # Initialize filter state with first measurement
            self._kf_x.x = np.array([[x], [0]])
            self._kf_y.x = np.array([[y], [0]])
            self._initialized = True

        # Predict and update
        self._kf_x.predict()
        self._kf_x.update(np.array([[x]]))
        self._kf_y.predict()
        self._kf_y.update(np.array([[y]]))

        smoothed_x = float(self._kf_x.x[0])
        smoothed_y = float(self._kf_y.x[0])

        # Clamp to valid range
        smoothed_x = max(0.0, min(1.0, smoothed_x))
        smoothed_y = max(0.0, min(1.0, smoothed_y))

        return smoothed_x, smoothed_y

    def _moving_average_update(self, x: float, y: float) -> Tuple[float, float]:
        """Fallback: simple moving average smoothing."""
        self._fallback_window.append((x, y))
        if len(self._fallback_window) > self._window_size:
            self._fallback_window.pop(0)

        avg_x = sum(p[0] for p in self._fallback_window) / len(self._fallback_window)
        avg_y = sum(p[1] for p in self._fallback_window) / len(self._fallback_window)
        return avg_x, avg_y

    def reset(self):
        """Reset the Kalman filter state."""
        self._initialized = False
        self._fallback_window = []
        if HAS_FILTERPY and self._kf_x is not None:
            self._kf_x.P *= 1.0
            self._kf_y.P *= 1.0
        logger.info("KalmanTracker reset")
