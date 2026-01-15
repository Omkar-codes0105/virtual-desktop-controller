"""Camera module for capturing video input."""
import cv2
from typing import Optional

class CameraHandler:
    """Handles webcam input and frame capture."""
    
    def __init__(self, camera_id: int = 0):
        """Initialize camera handler.
        
        Args:
            camera_id: Index of the camera device to use
        """
        self.camera_id = camera_id
        self.cap = None
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the camera.
        
        Returns:
            True if camera initialized successfully
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            if self.cap.isOpened():
                self.is_initialized = True
                return True
            return False
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def get_frame(self) -> Optional[tuple]:
        """Get a frame from the camera.
        
        Returns:
            Tuple of (success, frame) or (False, None)
        """
        if not self.is_initialized:
            return False, None
        return self.cap.read()
    
    def release(self) -> None:
        """Release the camera resource."""
        if self.cap is not None:
            self.cap.release()
            self.is_initialized = False

    def __del__(self):
        """Cleanup on object deletion."""
        self.release()
