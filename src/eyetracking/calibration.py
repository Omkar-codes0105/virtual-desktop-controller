"""9-point eye gaze calibration for iris-to-screen coordinate mapping."""
import logging
import numpy as np
from typing import List, Tuple, Optional, Dict

logger = logging.getLogger(__name__)


class CalibrationManager:
    """Manages 9-point eye calibration for gaze-to-screen mapping."""

    def __init__(self):
        """Initialize calibration manager."""
        self.calibration_points: List[Dict] = []
        self.mapping_matrix_x = None
        self.mapping_matrix_y = None
        self.is_calibrated = False
        logger.info("CalibrationManager initialized")

    def reset(self):
        """Reset calibration data."""
        self.calibration_points = []
        self.is_calibrated = False
        self.mapping_matrix_x = None
        self.mapping_matrix_y = None
        logger.info("Calibration reset")

    def collect_sample(self, screen_x: float, screen_y: float,
                       iris_data: Tuple[float, float]):
        """Collect a calibration sample.

        Args:
            screen_x: Normalized screen x coordinate (0-1)
            screen_y: Normalized screen y coordinate (0-1)
            iris_data: Tuple (x, y) of iris center in normalized coords
        """
        if not iris_data:
            return
        ix, iy = iris_data
        self.calibration_points.append({
            'screen': (screen_x, screen_y),
            'iris': (ix, iy)
        })
        logger.debug(f"Collected sample {len(self.calibration_points)}: Iris({ix:.3f},{iy:.3f})")

    def calibrate(self) -> bool:
        """Fit the mapping model using collected points.

        Uses linear regression: Screen = A * Iris + B

        Returns:
            True if calibration successful
        """
        if len(self.calibration_points) < 4:
            logger.warning(f"Not enough calibration points: have {len(self.calibration_points)}, need >= 4")
            return False

        try:
            iris_matrix = []
            screen_x_vec = []
            screen_y_vec = []

            for point in self.calibration_points:
                ix, iy = point['iris']
                sx, sy = point['screen']
                iris_matrix.append([ix, iy, 1])
                screen_x_vec.append(sx)
                screen_y_vec.append(sy)

            A = np.array(iris_matrix)
            Bx = np.array(screen_x_vec)
            By = np.array(screen_y_vec)

            # Least squares regression
            res_x = np.linalg.lstsq(A, Bx, rcond=None)
            res_y = np.linalg.lstsq(A, By, rcond=None)

            self.mapping_matrix_x = res_x[0]
            self.mapping_matrix_y = res_y[0]
            self.is_calibrated = True

            # Calculate residual error
            residuals_x = res_x[1] if len(res_x[1]) > 0 else [0]
            residuals_y = res_y[1] if len(res_y[1]) > 0 else [0]
            error_x = residuals_x[0] if len(residuals_x) > 0 else 0
            error_y = residuals_y[0] if len(residuals_y) > 0 else 0

            logger.info(f"Calibration successful with {len(self.calibration_points)} points")
            logger.info(f"  X coefficients: {self.mapping_matrix_x}")
            logger.info(f"  Y coefficients: {self.mapping_matrix_y}")
            logger.info(f"  Residual error: X={error_x:.6f}, Y={error_y:.6f}")
            return True

        except Exception as e:
            logger.error(f"Calibration failed: {e}")
            return False

    def map_to_screen(self, iris_data: Tuple[float, float]) -> Optional[Tuple[float, float]]:
        """Map iris coordinates to screen coordinates.

        Args:
            iris_data: Tuple (x, y) of iris position normalized

        Returns:
            Tuple (x, y) of screen position normalized or None
        """
        if not self.is_calibrated or not iris_data:
            return None

        try:
            ix, iy = iris_data
            v = np.array([ix, iy, 1])
            sx = np.dot(v, self.mapping_matrix_x)
            sy = np.dot(v, self.mapping_matrix_y)

            # Clamp to 0-1 range
            sx = max(0.0, min(1.0, sx))
            sy = max(0.0, min(1.0, sy))
            return sx, sy

        except Exception as e:
            logger.error(f"Mapping error: {e}")
            return None

    def get_calibration_points(self) -> List[Tuple[float, float]]:
        """Get standard 9-point calibration grid.

        Returns:
            List of (x, y) normalized screen coordinates
        """
        return [
            (0.1, 0.1), (0.5, 0.1), (0.9, 0.1),  # Top row
            (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),  # Middle row
            (0.1, 0.9), (0.5, 0.9), (0.9, 0.9),  # Bottom row
        ]
