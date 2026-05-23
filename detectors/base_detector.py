import numpy as np

class BaseDetector:
    """
    Base class for all specific joint-posture and exercise detectors.
    Provides standard 2D joint angle geometry helper methods and handles state trackers.
    """
    def __init__(self):
        self.reps = 0
        self.stage = "up"
        self.feedback = "Get ready! Align your full body in the camera frame."
        self.last_rep_time = 0.0  # Timestamp of last completed rep to prevent double counting
        
    def calculate_angle(self, a, b, c):
        """
        Calculates the angle (in degrees) at joint B formed by points A, B, and C.
        Each point should be a tuple (x, y) of normalized coordinates.
        """
        # Convert points to numpy arrays
        a = np.array([a[0], a[1]])
        b = np.array([b[0], b[1]])
        c = np.array([c[0], c[1]])
        
        # Calculate angle using arctan2
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        # Normalize to 0-180 range
        if angle > 180.0:
            angle = 360.0 - angle
            
        return angle

    def process(self, landmarks):
        """
        Processes normalized landmarks, updates internal states (reps, stage, feedback)
        and returns a dictionary of angles and statuses.
        Must be implemented by child classes.
        """
        raise NotImplementedError("Each exercise detector must implement the process method.")
