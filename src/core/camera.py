import cv2
import threading
import logging
import time
from typing import Optional, Tuple, Any

logger = logging.getLogger(__name__)

class Camera:
    def __init__(self, width: int = 1280, height: int = 720, fps: int = 30, camera_id: int = 0):
        self.width = width
        self.height = height
        self.fps = fps
        self.camera_id = camera_id
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.current_frame = None
        self.lock = threading.Lock()

    def start(self):
        """Start the camera capture in a separate thread."""
        if self.is_running:
            return

        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                raise RuntimeError(f"Could not open camera {self.camera_id}")
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            self.is_running = True
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
            logger.info(f"Camera started: {self.width}x{self.height} @ {self.fps}fps")
        except Exception as e:
            logger.error(f"Failed to start camera: {e}")
            self.is_running = False

    def stop(self):
        """Stop the camera capture."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        
        if self.cap:
            self.cap.release()
        logger.info("Camera stopped")

    def _capture_loop(self):
        """Dedicated thread for frame capturing."""
        while self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.current_frame = frame
            else:
                logger.warning("Failed to grab frame")
                time.sleep(0.1)
            
            # Simple FPS limiting if needed, though waitKey/sleep in loop is better handled
            # by just reading as fast as camera provides or letting opencv handle it.
            time.sleep(0.001)

    def get_frame(self) -> Tuple[bool, Optional[Any]]:
        """Get the latest frame from the buffer."""
        with self.lock:
            if self.current_frame is None:
                return False, None
            return True, self.current_frame.copy()
