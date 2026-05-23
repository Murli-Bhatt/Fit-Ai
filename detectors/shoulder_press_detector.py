from detectors.base_detector import BaseDetector
import time

class ShoulderPressDetector(BaseDetector):
    """
    Overhead shoulder press extension tracker and symmetry coach.
    """
    def __init__(self):
        super().__init__()
        self.stage = "down"
        
    def process(self, landmarks):
        # Shoulder (11/12), Elbow (13/14), Wrist (15/16)
        left_shoulder = landmarks[11]
        left_elbow = landmarks[13]
        left_wrist = landmarks[15]
        left_hip = landmarks[23]
        
        right_shoulder = landmarks[12]
        right_elbow = landmarks[14]
        right_wrist = landmarks[16]
        right_hip = landmarks[24]

        # Orientation Validation: Must be vertical (standing)
        if left_shoulder.visibility > right_shoulder.visibility:
            x_diff = abs(left_shoulder.x - left_hip.x)
            y_diff = abs(left_shoulder.y - left_hip.y)
        else:
            x_diff = abs(right_shoulder.x - right_hip.x)
            y_diff = abs(right_shoulder.y - right_hip.y)
            
        if x_diff > y_diff:
            self.feedback = "Positioning Check: Please stand upright for Shoulder Press."
            return {
                "elbow_l": 180.0,
                "elbow_r": 180.0,
                "extension": "Low",
                "symmetry": "Balanced"
            }
            
        # Select active side to check wrist-elbow posture (Shoulder Press requires hands up/wrists above elbows)
        if left_elbow.visibility > right_elbow.visibility:
            are_wrists_down = left_wrist.y > (left_elbow.y + 0.05)
        else:
            are_wrists_down = right_wrist.y > (right_elbow.y + 0.05)

        if are_wrists_down:
            self.feedback = "Positioning Check: Wrists are below elbows. Keep wrists stacked above elbows to press."
            return {
                "elbow_l": 180.0,
                "elbow_r": 180.0,
                "extension": "Low",
                "symmetry": "Balanced"
            }
        
        elbow_l = self.calculate_angle(
            (left_shoulder.x, left_shoulder.y),
            (left_elbow.x, left_elbow.y),
            (left_wrist.x, left_wrist.y)
        )
        elbow_r = self.calculate_angle(
            (right_shoulder.x, right_shoulder.y),
            (right_elbow.x, right_elbow.y),
            (right_wrist.x, right_wrist.y)
        )
        
        # Select active side based on visibility score
        if left_elbow.visibility > right_elbow.visibility:
            active_angle = elbow_l
        else:
            active_angle = elbow_r
            
        down_threshold = 90.0
        up_threshold = 165.0
        
        # Symmetry check: elbows angles should be within 18 degrees of each other
        is_symmetrical = abs(elbow_l - elbow_r) < 18.0
        
        if active_angle < down_threshold:
            self.stage = "down"
            self.feedback = "Weights lowered to shoulders. Press overhead!"
        elif self.stage == "down" and active_angle > up_threshold:
            current_time = time.time()
            if current_time - self.last_rep_time > 1.2:
                self.reps += 1
                self.last_rep_time = current_time
                self.stage = "up"
                if not is_symmetrical:
                    self.feedback = "Good rep! But try to push symmetrically on both sides."
                else:
                    self.feedback = "Excellent rep! Fully locked out symmetrically."
        else:
            if self.stage == "up":
                if active_angle < up_threshold and active_angle > down_threshold:
                    self.feedback = "Lowering down... keep wrists stacked above elbows."
                else:
                    self.feedback = "Extend your arms overhead to start the press!"
                    
        return {
            "elbow_l": elbow_l,
            "elbow_r": elbow_r,
            "extension": "High" if active_angle >= up_threshold else "Low",
            "symmetry": "Balanced" if is_symmetrical else "Asymmetrical"
        }
