import mediapipe as mp
print(f"MediaPipe version: {mp.__version__}")
try:
    print(f"Has solutions: {hasattr(mp, 'solutions')}")
    if hasattr(mp, 'solutions'):
        print(f"Solutions: {dir(mp.solutions)}")
        print(f"Hands avaiable: {hasattr(mp.solutions, 'hands')}")
    else:
        print("Trying explicit import...")
        import mediapipe.python.solutions as solutions
        print("Explicit import success")
except Exception as e:
    print(f"Error: {e}")
