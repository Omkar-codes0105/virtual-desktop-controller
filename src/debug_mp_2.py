import mediapipe as mp
import os
import sys

print(f"Python executable: {sys.executable}")
print(f"MediaPipe version: {mp.__version__}")
try:
    print(f"MediaPipe file: {mp.__file__}")
    print(f"MediaPipe dir: {os.path.dirname(mp.__file__)}")
    print(f"Dir(mp): {dir(mp)}")
    
    # List contents of mediapipe directory
    mp_path = os.path.dirname(mp.__file__)
    print(f"Contents of {mp_path}:")
    for item in os.listdir(mp_path):
        print(f"  {item}")
        
except Exception as e:
    print(f"Error inspecting mp: {e}")
