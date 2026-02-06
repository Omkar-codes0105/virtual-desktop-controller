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
from core.utils import resize_frame

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Desktop Controller")
        self.setGeometry(100, 100, 1280, 720)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)
        
        self.status_label = QLabel("Initializing...")
        self.layout.addWidget(self.status_label)
        
        # Initialize components
        self.config = ConfigManager()
        self.camera = Camera()
        self.gesture_recognizer = GestureRecognizer()
        self.eye_tracker = EyeTracker()
        
        self.camera.start()
        
        # Timer for UI updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30) # ~30 FPS
        
    def update_frame(self):
        ret, frame = self.camera.get_frame()
        if not ret:
            return
        
        # Process frame
        gesture_data = self.gesture_recognizer.process_frame(frame)
        tracker_data = self.eye_tracker.process_frame(frame)
        
        # Draw Overlays
        if gesture_data['landmarks']:
            self.gesture_recognizer.draw_landmarks(frame, gesture_data['landmarks'])
            cv2.putText(frame, f"Gesture: {gesture_data['gesture']}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        if tracker_data['gaze_point']:
            # self.eye_tracker.draw_landmarks(frame, tracker_data['landmarks'])
            gx, gy = tracker_data['gaze_point']
            h, w, _ = frame.shape
            cv2.circle(frame, (int(gx * w), int(gy * h)), 10, (0, 0, 255), -1)
            cv2.putText(frame, f"Gaze: ({gx:.2f}, {gy:.2f})", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Update status
        status_text = f"FPS: {self.camera.fps} | Hardware: {self.config.hardware_tier}"
        self.status_label.setText(status_text)
        
        # Display in UI
        self.display_image(frame)

    def display_image(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.camera.stop()
        event.accept()

    def run(self):
        # This is a bit unusual since QApplication usually runs exec_()
        # But keeping it here if main.py expects a run method
        self.show()
