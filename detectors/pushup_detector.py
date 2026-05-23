from detectors.base_detector import BaseDetector
import time

class PushupDetector(BaseDetector):
    """
    Push-up depth and body alignment tracker.
    """
    def __init__(self):
        super().__init__()
        self.stage = "up"
        
    def process(self, landmarks):
        # Shoulder (11/12), Elbow (13/14), Wrist (15/16)
        # Hip (23/24), Ankle (27/28)
        left_shoulder = landmarks[11]
        left_elbow = landmarks[13]
        left_wrist = landmarks[15]
        left_hip = landmarks[23]
        left_ankle = landmarks[27]
        
        right_shoulder = landmarks[12]
        right_elbow = landmarks[14]
        right_wrist = landmarks[16]
        right_hip = landmarks[24]
        right_ankle = landmarks[28]

        # Orientation Validation: Must be horizontal (plank/push-up)
        if left_shoulder.visibility > right_shoulder.visibility:
            x_diff = abs(left_shoulder.x - left_hip.x)
            y_diff = abs(left_shoulder.y - left_hip.y)
        else:
            x_diff = abs(right_shoulder.x - right_hip.x)
            y_diff = abs(right_shoulder.y - right_hip.y)
            
        if y_diff > x_diff:
            self.feedback = "Positioning Check: Please assume a horizontal plank position for Push-ups."
            return {
                "elbow": 180.0,
                "torso": 180.0,
                "depth": "Top Plank",
                "symmetry": "Balanced"
            }
        
        # Max visibility side selection
        if left_elbow.visibility > right_elbow.visibility:
            elbow_angle = self.calculate_angle(
                (left_shoulder.x, left_shoulder.y),
                (left_elbow.x, left_elbow.y),
                (left_wrist.x, left_wrist.y)
            )
            torso_angle = self.calculate_angle(
                (left_shoulder.x, left_shoulder.y),
                (left_hip.x, left_hip.y),
                (left_ankle.x, left_ankle.y)
            )
        else:
            elbow_angle = self.calculate_angle(
                (right_shoulder.x, right_shoulder.y),
                (right_elbow.x, right_elbow.y),
                (right_wrist.x, right_wrist.y)
            )
            torso_angle = self.calculate_angle(
                (right_shoulder.x, right_shoulder.y),
                (right_hip.x, right_hip.y),
                (right_ankle.x, right_ankle.y)
            )
            
        down_threshold = 95.0
        up_threshold = 160.0
        
        # Rigidity check: Flat back is between 165 and 190 degrees
        is_flat_back = 165.0 <= torso_angle <= 190.0
        
        if elbow_angle < down_threshold:
            self.stage = "down"
            if not is_flat_back:
                if torso_angle < 165.0:
                    self.feedback = "Form Warning: Keep core tight! Don't let your hips sag."
                else:
                    self.feedback = "Form Warning: Hips too high! Keep body in a straight line."
            else:
                self.feedback = "Excellent pushup depth! Now push up."
        elif self.stage == "down" and elbow_angle > up_threshold:
            current_time = time.time()
            if current_time - self.last_rep_time > 1.2:
                self.reps += 1
                self.last_rep_time = current_time
                self.stage = "up"
                self.feedback = "Good rep! Push fully up and extend."
        else:
            if self.stage == "up":
                if elbow_angle < up_threshold and elbow_angle > down_threshold:
                    self.feedback = "Lowering down... keep your head neutral."
                else:
                    self.feedback = "Ready! Engage your core and start the push-up."
                    
        return {
            "elbow": elbow_angle,
            "torso": torso_angle,
            "depth": "Chest to Floor" if elbow_angle <= 90 else ("Moderate" if elbow_angle <= 120 else "Top Plank"),
            "symmetry": "Balanced" if is_flat_back else "Sagging Hips"
        }
