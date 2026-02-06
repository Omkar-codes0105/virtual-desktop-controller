import cv2
import logging
from typing import Dict, Any, Optional

try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except ImportError:
    HAS_MEDIAPIPE = False

logger = logging.getLogger(__name__)

class GestureRecognizer:
    def __init__(self, static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        self.mp_hands = None
        self.hands = None
        self.mp_draw = None
        
        if HAS_MEDIAPIPE and hasattr(mp, 'solutions'):
            try:
                self.mp_hands = mp.solutions.hands
                self.hands = self.mp_hands.Hands(
                    static_image_mode=static_image_mode,
                    max_num_hands=max_num_hands,
                    min_detection_confidence=min_detection_confidence,
                    min_tracking_confidence=min_tracking_confidence
                )
                self.mp_draw = mp.solutions.drawing_utils
            except AttributeError:
                logger.error("MediaPipe solutions not found.")
        else:
            logger.warning("MediaPipe not installed or solutions missing. Gesture recognition disabled.")

    def process_frame(self, frame: Any) -> Dict[str, Any]:

        self.current_gesture = None
        self.confidence = 0.0

    def process_frame(self, frame: Any) -> Dict[str, Any]:
        """Process the frame and return detected gestures."""
        if frame is None or not self.hands:
            return {'gesture': None, 'landmarks': None, 'confidence': 0.0, 'handedness': None}

        # MediaPipe requires RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gesture_data = {
            'gesture': None,
            'landmarks': None,
            'confidence': 0.0,
            'handedness': None
        }

        if results.multi_hand_landmarks:
            # For simplicity, just take the first hand
            hand_landmarks = results.multi_hand_landmarks[0]
            gesture_data['landmarks'] = hand_landmarks
            
            # Simple gesture logic (placeholder for detailed logic)
            self.current_gesture = self._classify_gesture(hand_landmarks)
            gesture_data['gesture'] = self.current_gesture
            gesture_data['confidence'] = 0.9 # Placeholder confidence
            
            if results.multi_handedness:
                gesture_data['handedness'] = results.multi_handedness[0].classification[0].label

        return gesture_data

    def _classify_gesture(self, landmarks):
        """Simple rule-based gesture classification."""
        # Extract meaningful landmarks
        # 0: Wrist, 8: Index Tip, 12: Middle Tip, etc.
        
        # Example: Check if hand is open or closed (fist)
        # Check if fingertips are above (lower y value) their respective PIP joints
        # Note: Origin (0,0) is top-left.
        
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        
        extended_fingers = 0
        for tip, pip in zip(tips, pips):
            if landmarks.landmark[tip].y < landmarks.landmark[pip].y:
                extended_fingers += 1
                
        # Thumb is a bit different, checking x relative to IP
        # Assuming right hand for simplicity of example logic
        if landmarks.landmark[4].x < landmarks.landmark[3].x: # Right hand thumb open to left
             extended_fingers += 1
        elif landmarks.landmark[4].x > landmarks.landmark[3].x: # Left hand thumb open to right
             extended_fingers += 1

        if extended_fingers >= 4:
            return "OPEN_PALM"
        elif extended_fingers == 0:
            return "CLOSED_FIST"
        elif extended_fingers == 1:
             # Check if it's index
             if landmarks.landmark[8].y < landmarks.landmark[6].y:
                 return "POINTING"
        
        return "UNKNOWN"

    def draw_landmarks(self, frame, landmarks):
        if landmarks:
            self.mp_draw.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)
