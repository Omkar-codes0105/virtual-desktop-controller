"""Gesture recognition using MediaPipe Tasks API."""
import cv2
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

try:
    import mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import BaseOptions
    from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions
    from mediapipe.tasks.python.vision import RunningMode
    HAS_MEDIAPIPE = True
except ImportError:
    HAS_MEDIAPIPE = False

logger = logging.getLogger(__name__)


class GestureRecognizer:
    """Hand gesture recognition using MediaPipe Tasks API."""

    def __init__(self, min_detection_confidence: float = 0.7,
                 min_tracking_confidence: float = 0.5,
                 max_num_hands: int = 1):
        """Initialize gesture recognizer.

        Args:
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for tracking
            max_num_hands: Maximum number of hands to detect
        """
        self.landmarker = None
        self._timestamp_ms = 0
        self.current_gesture = None
        self.confidence = 0.0

        if not HAS_MEDIAPIPE:
            logger.error("MediaPipe not installed. Gesture recognition disabled.")
            return

        model_path = self._find_model_file()
        if not model_path:
            logger.error("Hand landmarker model not found. Gesture recognition disabled.")
            return

        try:
            options = HandLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=str(model_path)),
                running_mode=RunningMode.VIDEO,
                num_hands=max_num_hands,
                min_hand_detection_confidence=min_detection_confidence,
                min_hand_presence_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence
            )
            self.landmarker = HandLandmarker.create_from_options(options)
            logger.info(f"GestureRecognizer initialized with Tasks API model: {model_path}")
        except Exception as e:
            logger.error(f"Failed to initialize HandLandmarker: {e}")
            self.landmarker = None

    def _find_model_file(self) -> Optional[Path]:
        """Find the hand_landmarker.task model file.

        Returns:
            Path to model file or None if not found
        """
        project_root = Path(__file__).parent.parent.parent
        search_paths = [
            project_root / "models" / "hand_landmarker.task",
            project_root / "hand_landmarker.task",
            Path("models/hand_landmarker.task"),
            Path("hand_landmarker.task"),
        ]
        for path in search_paths:
            if path.exists():
                return path.resolve()
        logger.warning(f"Model file not found. Searched: {[str(p) for p in search_paths]}")
        return None

    def process_frame(self, frame: Any) -> Dict[str, Any]:
        """Process frame and detect gestures.

        Args:
            frame: BGR image from OpenCV

        Returns:
            Dictionary with gesture data:
                gesture (str or None), landmarks (list or None),
                confidence (float), handedness (str or None)
        """
        if frame is None or self.landmarker is None:
            return {'gesture': None, 'landmarks': None, 'confidence': 0.0, 'handedness': None}

        try:
            # Convert to RGB (MediaPipe requirement)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Create MediaPipe Image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            # Increment timestamp for video mode
            self._timestamp_ms += 33  # ~30 FPS
            # Detect hands
            results = self.landmarker.detect_for_video(mp_image, self._timestamp_ms)

            gesture_data = {'gesture': None, 'landmarks': None, 'confidence': 0.0, 'handedness': None}

            if results.hand_landmarks and len(results.hand_landmarks) > 0:
                # Process first detected hand
                hand_landmarks = results.hand_landmarks[0]
                gesture_data['landmarks'] = hand_landmarks
                # Classify gesture
                gesture, confidence = self._classify_gesture(hand_landmarks)
                gesture_data['gesture'] = gesture
                gesture_data['confidence'] = confidence

            if results.handedness and len(results.handedness) > 0:
                gesture_data['handedness'] = results.handedness[0][0].category_name

            return gesture_data

        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return {'gesture': None, 'landmarks': None, 'confidence': 0.0, 'handedness': None}

    def _classify_gesture(self, landmarks: List) -> tuple:
        """Classify gesture from hand landmarks.

        Args:
            landmarks: List of hand landmarks

        Returns:
            Tuple of (gesture_name, confidence)
        """
        try:
            # Landmark indices
            THUMB_TIP = 4
            INDEX_TIP = 8
            MIDDLE_TIP = 12
            RING_TIP = 16
            PINKY_TIP = 20
            INDEX_PIP = 6
            MIDDLE_PIP = 10
            RING_PIP = 14
            PINKY_PIP = 18
            THUMB_IP = 3

            extended_fingers = 0

            # Check index, middle, ring, pinky: tip above PIP = extended
            finger_tips = [INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
            finger_pips = [INDEX_PIP, MIDDLE_PIP, RING_PIP, PINKY_PIP]
            for tip, pip in zip(finger_tips, finger_pips):
                if landmarks[tip].y < landmarks[pip].y:
                    extended_fingers += 1

            # Check thumb: different logic - check x distance
            thumb_extended = abs(landmarks[THUMB_TIP].x - landmarks[THUMB_IP].x) > 0.04
            if thumb_extended:
                extended_fingers += 1

            if extended_fingers == 0:
                return 'CLOSED_FIST', 0.9
            elif extended_fingers >= 4:
                return 'OPEN_PALM', 0.9
            elif extended_fingers == 1:
                # Check if it's index finger
                if landmarks[INDEX_TIP].y < landmarks[INDEX_PIP].y:
                    return 'POINTING', 0.9
            elif extended_fingers == 2:
                index_extended = landmarks[INDEX_TIP].y < landmarks[INDEX_PIP].y
                # Check for pinch (thumb + index)
                if thumb_extended and index_extended:
                    dist = ((landmarks[THUMB_TIP].x - landmarks[INDEX_TIP].x) ** 2 +
                            (landmarks[THUMB_TIP].y - landmarks[INDEX_TIP].y) ** 2) ** 0.5
                    if dist < 0.05:
                        return 'PINCH', 0.9
                    else:
                        return 'PEACE_SIGN', 0.8

            return 'UNKNOWN', 0.5

        except Exception as e:
            logger.error(f"Error classifying gesture: {e}")
            return 'ERROR', 0.0

    def draw_landmarks(self, frame, landmarks):
        """Draw hand landmarks on frame.

        Args:
            frame: Image to draw on
            landmarks: Hand landmarks to draw
        """
        if landmarks is None:
            return
        try:
            h, w, _ = frame.shape
            HAND_CONNECTIONS = [
                (0, 1), (1, 2), (2, 3), (3, 4),    # Thumb
                (0, 5), (5, 6), (6, 7), (7, 8),    # Index
                (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
                (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
                (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
                (5, 9), (9, 13), (13, 17)           # Palm
            ]
            # Draw connections
            for connection in HAND_CONNECTIONS:
                start_idx, end_idx = connection
                start = landmarks[start_idx]
                end = landmarks[end_idx]
                start_point = (int(start.x * w), int(start.y * h))
                end_point = (int(end.x * w), int(end.y * h))
                cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
            # Draw landmarks
            for landmark in landmarks:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        except Exception as e:
            logger.error(f"Error drawing landmarks: {e}")
