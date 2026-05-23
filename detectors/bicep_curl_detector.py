from detectors.base_detector import BaseDetector
import time

class BicepCurlDetector(BaseDetector):
    """
    Bicep Curl rep tracker and shoulder/elbow stability coach.
    """
    def __init__(self):
        super().__init__()
        self.stage = "extended"
        
    def process(self, landmarks):
        # Shoulder (11/12), Elbow (13/14), Wrist (15/16), Hip (23/24)
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
            self.feedback = "Positioning Check: Please stand upright for Bicep Curls."
            return {
                "elbow_l": 180.0,
                "elbow_r": 180.0,
                "stability": "Low",
                "range": "Full Extension"
            }
            
        # Select active side to check overhead position (e.g. Shoulder Press)
        if left_elbow.visibility > right_elbow.visibility:
            is_overhead = (left_elbow.y < left_shoulder.y) or (left_wrist.y < left_shoulder.y)
        else:
            is_overhead = (right_elbow.y < right_shoulder.y) or (right_wrist.y < right_shoulder.y)

        if is_overhead:
            self.feedback = "Positioning Check: Elbows or wrists raised overhead. Please keep elbows at your side for Bicep Curls."
            return {
                "elbow_l": 180.0,
                "elbow_r": 180.0,
                "stability": "Low",
                "range": "Full Extension"
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
        
        # Stability: Check elbow swing angle (Hip - Shoulder - Elbow)
        # Ideally elbows should stay locked close to the side of the body (< 18 degrees)
        elbow_l_flare = self.calculate_angle(
            (left_hip.x, left_hip.y),
            (left_shoulder.x, left_shoulder.y),
            (left_elbow.x, left_elbow.y)
        )
        elbow_r_flare = self.calculate_angle(
            (right_hip.x, right_hip.y),
            (right_shoulder.x, right_shoulder.y),
            (right_elbow.x, right_elbow.y)
        )
        
        # Select active arm based on maximum elbow joint visibility
        if left_elbow.visibility > right_elbow.visibility:
            active_angle = elbow_l
            active_flare = elbow_l_flare
        else:
            active_angle = elbow_r
            active_flare = elbow_r_flare
            
        down_threshold = 150.0
        up_threshold = 45.0
        
        stability = "High"
        if active_flare > 30.0:
            stability = "Low"
        elif active_flare > 18.0:
            stability = "Medium"
            
        if active_angle < up_threshold:
            self.stage = "flexed"
            if stability == "Low":
                self.feedback = "Form Warning: Keep elbows locked at your side! Don't swing."
            else:
                self.feedback = "Peak contraction reached! Control the descent."
        elif self.stage == "flexed" and active_angle > down_threshold:
            current_time = time.time()
            if current_time - self.last_rep_time > 1.2:
                self.reps += 1
                self.last_rep_time = current_time
                self.stage = "extended"
                self.feedback = "Excellent rep! Fully stretch your bicep."
        else:
            if self.stage == "extended":
                if active_angle > down_threshold:
                    self.feedback = "Fully extended. Start the curl!"
                else:
                    self.feedback = "Curling up... keep upper arms stable."
                    
        return {
            "elbow_l": elbow_l,
            "elbow_r": elbow_r,
            "stability": stability,
            "range": "Full Extension" if active_angle >= down_threshold else ("Peak Contraction" if active_angle <= up_threshold else "Mid Range")
        }
