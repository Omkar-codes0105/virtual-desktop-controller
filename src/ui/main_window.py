"""Main window for Virtual Desktop Controller using MediaPipe Tasks API."""
import sys
import cv2
import logging
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

from core.camera import Camera
from core.config_manager import ConfigManager
from gesture.gesture_recognizer import GestureRecognizer
from eyetracking.eye_tracker import EyeTracker

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window with component-based architecture and graceful error handling."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Desktop Controller")
        self.setGeometry(100, 100, 1280, 720)

        # Setup UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("font-size: 14px; padding: 10px")
        self.layout.addWidget(self.status_label)

        # Component status tracking
        self.components_status = {
            'camera': False,
            'gesture': False,
            'eye_tracking': False
        }

        # Initialize components with error handling
        self.config = ConfigManager()
        self.camera = None
        self.gesture_recognizer = None
        self.eye_tracker = None

        self.initialize_components()

        # Timer for UI updates
        if self.components_status['camera']:
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)  # ~30 FPS
            logger.info("UI timer started")
        else:
            self.status_label.setText("ERROR: Camera failed to initialize")
            logger.error("Cannot start UI timer - camera not available")

    def initialize_components(self):
        """Initialize all components with graceful error handling."""
        # Initialize Camera
        try:
            self.camera = Camera()
            self.camera.start()
            self.components_status['camera'] = True
            logger.info("Camera initialized")
        except Exception as e:
            logger.error(f"Camera initialization failed: {e}")
            self.status_label.setText(f"Camera Error: {e}")

        # Initialize Gesture Recognizer
        try:
            self.gesture_recognizer = GestureRecognizer()
            if self.gesture_recognizer.landmarker is not None:
                self.components_status['gesture'] = True
                logger.info("Gesture recognizer initialized")
            else:
                logger.warning("Gesture recognizer disabled - model missing")
        except Exception as e:
            logger.error(f"Gesture recognizer initialization failed: {e}")

        # Initialize Eye Tracker
        try:
            self.eye_tracker = EyeTracker()
            if self.eye_tracker.landmarker is not None:
                self.components_status['eye_tracking'] = True
                logger.info("Eye tracker initialized")
            else:
                logger.warning("Eye tracker disabled - model missing")
        except Exception as e:
            logger.error(f"Eye tracker initialization failed: {e}")

        # Log final status
        active = [k for k, v in self.components_status.items() if v]
        logger.info(f"Active components: {', '.join(active)}")

    def update_frame(self):
        """Update frame with gesture and eye tracking overlays."""
        if not self.components_status['camera']:
            return

        ret, frame = self.camera.get_frame()
        if not ret or frame is None:
            return

        # Process eye tracking
        tracker_data = {'gaze_point': None, 'landmarks': None}
        if self.components_status['eye_tracking']:
            try:
                tracker_data = self.eye_tracker.process_frame(frame)
            except Exception as e:
                logger.error(f"Eye tracking error: {e}")

        # Process gesture recognition
        gesture_data = {'gesture': None, 'landmarks': None, 'confidence': 0.0}
        if self.components_status['gesture']:
            try:
                gesture_data = self.gesture_recognizer.process_frame(frame)
            except Exception as e:
                logger.error(f"Gesture processing error: {e}")

        # Draw overlays
        if gesture_data['landmarks']:
            self.gesture_recognizer.draw_landmarks(frame, gesture_data['landmarks'])
            if gesture_data['gesture']:
                text = f"{gesture_data['gesture']} {gesture_data['confidence']:.2f}"
                cv2.putText(frame, text, (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if tracker_data['gaze_point']:
            gx, gy = tracker_data['gaze_point']
            h, w, _ = frame.shape
            px, py = int(gx * w), int(gy * h)
            cv2.circle(frame, (px, py), 10, (0, 0, 255), -1)
            cv2.circle(frame, (px, py), 15, (0, 0, 255), 2)
            text = f"Gaze ({gx:.2f}, {gy:.2f})"
            cv2.putText(frame, text, (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Update status
        active = [k for k, v in self.components_status.items() if v]
        status_text = f"Active: {', '.join(active)}"
        if self.components_status['camera'] and hasattr(self.camera, 'fps'):
            status_text = f"FPS: {self.camera.fps} | " + status_text
        self.status_label.setText(status_text)

        # Display in UI
        self.display_image(frame)

    def display_image(self, frame):
        """Convert and display OpenCV frame in Qt label."""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        """Clean up resources on close."""
        if self.camera:
            self.camera.stop()
        event.accept()

    def run(self):
        """Show the main window."""
        self.show()
