from detectors.base_detector import BaseDetector
import time

class LungeDetector(BaseDetector):
    """
    Lead front knee depth and torso upright lunge posture coach.
    """
    def __init__(self):
        super().__init__()
        self.stage = "up"
        
    def process(self, landmarks):
        # Shoulder (11/12), Hip (23/24), Knee (25/26), Ankle (27/28)
        left_shoulder = landmarks[11]
        left_hip = landmarks[23]
        left_knee = landmarks[25]
        left_ankle = landmarks[27]
        
        right_shoulder = landmarks[12]
        right_hip = landmarks[24]
        right_knee = landmarks[26]
        right_ankle = landmarks[28]

        # Orientation Validation: Must be vertical (standing)
        if left_shoulder.visibility > right_shoulder.visibility:
            x_diff = abs(left_shoulder.x - left_hip.x)
            y_diff = abs(left_shoulder.y - left_hip.y)
        else:
            x_diff = abs(right_shoulder.x - right_hip.x)
            y_diff = abs(right_shoulder.y - right_hip.y)
            
        if x_diff > y_diff:
            self.feedback = "Positioning Check: Please stand upright for Lunges."
            return {
                "front_knee": 180.0,
                "back_knee": 180.0,
                "torso": "Straight",
                "depth": "Standing"
            }
            
        # Select stance check (Lunge requires legs spread apart horizontally)
        if left_ankle.visibility > 0.5 and right_ankle.visibility > 0.5:
            ankle_dist_x = abs(left_ankle.x - right_ankle.x)
            if ankle_dist_x < 0.12:
                self.feedback = "Positioning Check: Feet are too close together. Please assume a wide forward/backward lunge stance."
                return {
                    "front_knee": 180.0,
                    "back_knee": 180.0,
                    "torso": "Straight",
                    "depth": "Standing"
                }
        
        # Max visibility side selection
        if left_knee.visibility > right_knee.visibility:
            front_knee_angle = self.calculate_angle(
                (left_hip.x, left_hip.y),
                (left_knee.x, left_knee.y),
                (left_ankle.x, left_ankle.y)
            )
            back_knee_angle = front_knee_angle
            torso_angle = self.calculate_angle(
                (left_shoulder.x, left_shoulder.y),
                (left_hip.x, left_hip.y),
                (left_knee.x, left_knee.y)
            )
        else:
            front_knee_angle = self.calculate_angle(
                (right_hip.x, right_hip.y),
                (right_knee.x, right_knee.y),
                (right_ankle.x, right_ankle.y)
            )
            back_knee_angle = front_knee_angle
            torso_angle = self.calculate_angle(
                (right_shoulder.x, right_shoulder.y),
                (right_hip.x, right_hip.y),
                (right_knee.x, right_knee.y)
            )
            
        down_threshold = 95.0
        up_threshold = 150.0
        
        # Lunge torso upright check
        is_torso_upright = torso_angle > 140.0
        
        if front_knee_angle < down_threshold:
            self.stage = "down"
            if not is_torso_upright:
                self.feedback = "Form Warning: Keep chest up! Avoid leaning forward too much."
            else:
                self.feedback = "Excellent depth! Now push back up."
        elif self.stage == "down" and front_knee_angle > up_threshold:
            current_time = time.time()
            if current_time - self.last_rep_time > 1.2:
                self.reps += 1
                self.last_rep_time = current_time
                self.stage = "up"
                self.feedback = "Solid rep! Prepare to step forward."
        else:
            if self.stage == "up":
                if front_knee_angle < up_threshold and front_knee_angle > down_threshold:
                    self.feedback = "Sinking into the lunge... keep back straight."
                else:
                    self.feedback = "Step forward and lower into a deep lunge."
                    
        return {
            "front_knee": front_knee_angle,
            "back_knee": back_knee_angle,
            "torso": "Straight" if is_torso_upright else "Leaning",
            "depth": "Deep Lunge" if front_knee_angle <= 95 else "Standing"
        }
