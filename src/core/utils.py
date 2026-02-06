import numpy as np
import cv2

def resize_frame(frame, width=None, height=None, inter=cv2.INTER_AREA):
    """Resize the image to the specified width and height."""
    dim = None
    (h, w) = frame.shape[:2]

    if width is None and height is None:
        return frame

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(frame, dim, interpolation=inter)

def map_range(value, in_min, in_max, out_min, out_max):
    """Map a value from one range to another."""
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def smoothing_factor(t_e, cutoff):
    """Calculate smoothing factor for One Euro Filter or similar."""
    r = 2 * np.pi * cutoff * t_e
    return r / (r + 1)

def exponential_smoothing(current, previous, alpha):
    """Simple exponential smoothing."""
    if previous is None:
        return current
    return alpha * current + (1 - alpha) * previous
