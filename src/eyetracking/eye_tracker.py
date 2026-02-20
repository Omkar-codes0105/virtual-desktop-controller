"""Eye tracking and gaze estimation using MediaPipe Tasks API."""
import cv2
import logging
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List

try:
    import mediapipe as mp
    from mediapipe.tasks.python import BaseOptions
    from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions
    from mediapipe.tasks.python.vision import RunningMode
    HAS_MEDIAPIPE = True
except ImportError:
    HAS_MEDIAPIPE = False

logger = logging.getLogger(__name__)


class EyeTracker:
    """Eye tracking and gaze estimation using MediaPipe Face Mesh."""

    # Iris landmark indices (MediaPipe Face Mesh with refined landmarks)
    LEFT_IRIS_CENTER = 468
    RIGHT_IRIS_CENTER = 473
    LEFT_EYE_LANDMARKS = [33, 133, 160, 159, 158, 144, 145, 153]
    RIGHT_EYE_LANDMARKS = [263, 362, 387, 386, 385, 373, 374, 380]

    def __init__(self, min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """Initialize eye tracker.

        Args:
            min_detection_confidence: Minimum confidence for face detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.landmarker = None
        self._timestamp_ms = 0
        self.current_gaze = None

        if not HAS_MEDIAPIPE:
            logger.error("MediaPipe not installed. Eye tracking disabled.")
            return

        model_path = self._find_model_file()
        if not model_path:
            logger.error("Face landmarker model not found. Eye tracking disabled.")
            return

        try:
            options = FaceLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=str(model_path)),
                running_mode=RunningMode.VIDEO,
                num_faces=1,
                min_face_detection_confidence=min_detection_confidence,
                min_face_presence_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence,
                output_face_blendshapes=False,
                output_facial_transformation_matrixes=False
            )
            self.landmarker = FaceLandmarker.create_from_options(options)
            logger.info(f"EyeTracker initialized with Tasks API model: {model_path.name}")
        except Exception as e:
            logger.error(f"Failed to initialize FaceLandmarker: {e}")
            self.landmarker = None

    def _find_model_file(self) -> Optional[Path]:
        """Find the face_landmarker.task model file.

        Returns:
            Path to model file or None if not found
        """
        project_root = Path(__file__).parent.parent.parent
        search_paths = [
            project_root / "models" / "face_landmarker.task",
            project_root / "face_landmarker.task",
            Path("models/face_landmarker.task"),
            Path("face_landmarker.task"),
        ]
        for path in search_paths:
            if path.exists():
                return path.resolve()
        logger.warning(f"Model file not found. Searched: {[str(p) for p in search_paths]}")
        return None

    def process_frame(self, frame: Any) -> Dict[str, Any]:
        """Process frame and estimate gaze.

        Args:
            frame: BGR image from OpenCV

        Returns:
            Dictionary with tracking data:
                gaze_point (tuple x,y normalized 0-1, or None),
                landmarks (face landmarks or None),
                iris_left (tuple x,y or None),
                iris_right (tuple x,y or None)
        """
        if frame is None or self.landmarker is None:
            return {'gaze_point': None, 'landmarks': None, 'iris_left': None, 'iris_right': None}

        try:
            # Convert to RGB (MediaPipe requirement)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Create MediaPipe Image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            # Increment timestamp for video mode
            self._timestamp_ms += 33  # ~30 FPS
            # Detect face
            results = self.landmarker.detect_for_video(mp_image, self._timestamp_ms)

            tracker_data = {
                'gaze_point': None,
                'landmarks': None,
                'iris_left': None,
                'iris_right': None
            }

            if results.face_landmarks and len(results.face_landmarks) > 0:
                face_landmarks = results.face_landmarks[0]
                tracker_data['landmarks'] = face_landmarks

                # Extract iris centers for gaze estimation
                left_iris = face_landmarks[self.LEFT_IRIS_CENTER]
                right_iris = face_landmarks[self.RIGHT_IRIS_CENTER]

                tracker_data['iris_left'] = (left_iris.x, left_iris.y)
                tracker_data['iris_right'] = (right_iris.x, right_iris.y)

                # Average iris positions for central gaze point
                gaze_x = (left_iris.x + right_iris.x) / 2
                gaze_y = (left_iris.y + right_iris.y) / 2
                tracker_data['gaze_point'] = (gaze_x, gaze_y)

            return tracker_data

        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return {'gaze_point': None, 'landmarks': None, 'iris_left': None, 'iris_right': None}

    def draw_landmarks(self, frame, landmarks):
        """Draw eye landmarks on frame (optional visualization).

        Args:
            frame: Image to draw on
            landmarks: Face landmarks to draw
        """
        if landmarks is None:
            return
        try:
            h, w, _ = frame.shape
            # Draw left eye landmarks
            for idx in self.LEFT_EYE_LANDMARKS:
                lm = landmarks[idx]
                cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 2, (0, 255, 0), -1)
            # Draw right eye landmarks
            for idx in self.RIGHT_EYE_LANDMARKS:
                lm = landmarks[idx]
                cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 2, (0, 255, 0), -1)
            # Draw iris centers
            left_iris = landmarks[self.LEFT_IRIS_CENTER]
            right_iris = landmarks[self.RIGHT_IRIS_CENTER]
            cv2.circle(frame, (int(left_iris.x * w), int(left_iris.y * h)), 5, (255, 0, 0), -1)
            cv2.circle(frame, (int(right_iris.x * w), int(right_iris.y * h)), 5, (255, 0, 0), -1)
        except Exception as e:
            logger.error(f"Error drawing landmarks: {e}")
