import cv2
import logging
import numpy as np
from typing import Dict, Any, Tuple

try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except ImportError:
    HAS_MEDIAPIPE = False

logger = logging.getLogger(__name__)

class EyeTracker:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_face_mesh = None
        self.face_mesh = None
        self.mp_draw = None
        self.draw_spec = None

        if HAS_MEDIAPIPE and hasattr(mp, 'solutions'):
             try:
                self.mp_face_mesh = mp.solutions.face_mesh
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=min_detection_confidence,
                    min_tracking_confidence=min_tracking_confidence
                )
                self.mp_draw = mp.solutions.drawing_utils
                self.draw_spec = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1)
             except AttributeError:
                logger.error("MediaPipe solutions not found.")
        else:
            logger.warning("MediaPipe not installed or solutions missing. Eye tracking disabled.")

    def process_frame(self, frame: Any) -> Dict[str, Any]:
        """Process the frame and estimate gaze."""
        if frame is None or not self.face_mesh:
            return {'gaze_point': None, 'landmarks': None}

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        tracker_data = {
            'gaze_point': None,  # (x, y) normalized 0-1
            'landmarks': None
        }

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            tracker_data['landmarks'] = landmarks
            
            # Simple gaze estimation finding iris center
            # Left Iris: 474, 475, 476, 477
            # Right Iris: 469, 470, 471, 472
            # Center of Left Iris: 473
            # Center of Right Iris: 468
            
            h, w, c = frame.shape
            left_iris = landmarks.landmark[473]
            right_iris = landmarks.landmark[468]
            
            # Average for central gaze (very rough approximation)
            gaze_x = (left_iris.x + right_iris.x) / 2
            gaze_y = (left_iris.y + right_iris.y) / 2
            
            tracker_data['gaze_point'] = (gaze_x, gaze_y)

        return tracker_data

    def draw_landmarks(self, frame, landmarks):
        if landmarks:
            # Draw only irises for performance/clarity or full mesh
            # self.mp_draw.draw_landmarks(frame, landmarks, self.mp_face_mesh.FACEMESH_IRISES, self.draw_spec, self.draw_spec)
            pass # Drawing handled by UI usually to avoid burning into frame if not needed
