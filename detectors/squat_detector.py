from detectors.base_detector import BaseDetector
import time

class SquatDetector(BaseDetector):
    """
    Squat movement detector and biomechanical form coach.
    """
    def __init__(self):
        super().__init__()
        self.stage = "up"
        
    def process(self, landmarks):
        # MediaPipe Pose Landmarks:
        # Left hip: 23, Left knee: 25, Left ankle: 27, Left shoulder: 11
        # Right hip: 24, Right knee: 26, Right ankle: 28, Right shoulder: 12
        
        left_hip = landmarks[23]
        left_knee = landmarks[25]
        left_ankle = landmarks[27]
        left_shoulder = landmarks[11]
        
        right_hip = landmarks[24]
        right_knee = landmarks[26]
        right_ankle = landmarks[28]
        right_shoulder = landmarks[12]

        # Orientation Validation: Must be vertical (standing)
        if left_shoulder.visibility > right_shoulder.visibility:
            x_diff = abs(left_shoulder.x - left_hip.x)
            y_diff = abs(left_shoulder.y - left_hip.y)
        else:
            x_diff = abs(right_shoulder.x - right_hip.x)
            y_diff = abs(right_shoulder.y - right_hip.y)
            
        if x_diff > y_diff:
            self.feedback = "Positioning Check: Please stand upright for Squats. Horizontal posture detected."
            return {
                "knee": 180.0,
                "hip": 180.0,
                "depth": "Standing",
                "back": "Neutral Spine"
            }
        
        # Cross-Exercise check: Bicep Curls / arm movement instead of Squats
        left_elbow = landmarks[13]
        left_wrist = landmarks[15]
        right_elbow = landmarks[14]
        right_wrist = landmarks[16]

        if left_knee.visibility > right_knee.visibility:
            selected_knee = self.calculate_angle(
                (left_hip.x, left_hip.y),
                (left_knee.x, left_knee.y),
                (left_ankle.x, left_ankle.y)
            )
            active_elbow = self.calculate_angle(
                (left_shoulder.x, left_shoulder.y),
                (left_elbow.x, left_elbow.y),
                (left_wrist.x, left_wrist.y)
            )
        else:
            selected_knee = self.calculate_angle(
                (right_hip.x, right_hip.y),
                (right_knee.x, right_knee.y),
                (right_ankle.x, right_ankle.y)
            )
            active_elbow = self.calculate_angle(
                (right_shoulder.x, right_shoulder.y),
                (right_elbow.x, right_elbow.y),
                (right_wrist.x, right_wrist.y)
            )

        if selected_knee > 160.0 and active_elbow < 60.0:
            self.feedback = "Form Check: Arm movement detected. Please perform Squats by bending your knees."
            return {
                "knee": selected_knee,
                "hip": 180.0,
                "depth": "Standing",
                "back": "Neutral Spine"
            }

        # Select knee with maximum visibility
        if left_knee.visibility > right_knee.visibility:
            selected_side = "Left"
            knee_angle = selected_knee
            # Spine/Torso check: Angle formed by shoulder, hip, knee on left side
            hip_angle = self.calculate_angle(
                (left_shoulder.x, left_shoulder.y),
                (left_hip.x, left_hip.y),
                (left_knee.x, left_knee.y)
            )
        else:
            selected_side = "Right"
            knee_angle = selected_knee
            # Spine/Torso check: Angle formed by shoulder, hip, knee on right side
            hip_angle = self.calculate_angle(
                (right_shoulder.x, right_shoulder.y),
                (right_hip.x, right_hip.y),
                (right_knee.x, right_knee.y)
            )
            
        # Core squat parameters:
        # Down (flexion) threshold: knee angle <= 100 degrees
        # Up (extension) threshold: knee angle >= 150 degrees
        down_threshold = 100.0
        up_threshold = 150.0
        
        # Form verification: Hip angle should be open enough (> 85 deg) to prevent rounding the lower back/leaning too far forward
        is_leaning_forward = hip_angle < 85.0
        
        if knee_angle < down_threshold:
            self.stage = "down"
            if is_leaning_forward:
                self.feedback = "Form Warning: Keep your chest up! Avoid leaning too far forward."
            else:
                self.feedback = "Excellent squat depth! Maintain control."
        elif self.stage == "down" and knee_angle > up_threshold:
            # Debounce completed reps by 1.2s to prevent multiple quick registers
            current_time = time.time()
            if current_time - self.last_rep_time > 1.2:
                self.reps += 1
                self.last_rep_time = current_time
                self.stage = "up"
                self.feedback = "Good rep! Stand straight and prepare for the next."
        else:
            # Provide real-time intermediate guidance
            if self.stage == "up":
                if knee_angle < up_threshold and knee_angle > down_threshold:
                    self.feedback = "Descending... keep core engaged!"
                else:
                    self.feedback = "Ready! Stand straight and start the squat."
                    
        # Return biometrics formatted for squats.py gauges
        return {
            "knee": knee_angle,
            "hip": hip_angle,
            "depth": "Deep Squat" if knee_angle <= 95 else ("Parallel" if knee_angle <= 110 else "Standing"),
            "back": "Leaning Forward" if is_leaning_forward else "Neutral Spine"
        }
