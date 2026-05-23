from detectors.base_detector import BaseDetector
import time

class PlankDetector(BaseDetector):
    """
    Sustained plank holding duration and postural alignment tracker.
    """
    def __init__(self):
        super().__init__()
        self.plank_start_time = None
        self.last_timer_tick = None
        self.hold_time = 0.0
        self.stage = "setup"
        
    def process(self, landmarks):
        # Shoulder (11/12), Elbow (13/14), Hip (23/24), Ankle (27/28), Wrist (15/16)
        left_shoulder = landmarks[11]
        left_elbow = landmarks[13]
        left_hip = landmarks[23]
        left_ankle = landmarks[27]
        left_wrist = landmarks[15]
        
        right_shoulder = landmarks[12]
        right_elbow = landmarks[14]
        right_hip = landmarks[24]
        right_ankle = landmarks[28]
        right_wrist = landmarks[16]

        # Orientation Validation: Must be horizontal (plank)
        if left_shoulder.visibility > right_shoulder.visibility:
            x_diff = abs(left_shoulder.x - left_hip.x)
            y_diff = abs(left_shoulder.y - left_hip.y)
        else:
            x_diff = abs(right_shoulder.x - right_hip.x)
            y_diff = abs(right_shoulder.y - right_hip.y)
            
        if y_diff > x_diff:
            self.feedback = "Positioning Check: Please assume a horizontal plank position."
            self.stage = "setup"
            self.plank_start_time = None
            self.last_timer_tick = None
            return {
                "hip": 180.0,
                "elbow": 90.0,
                "stability": "Sub-optimal",
                "duration": int(self.hold_time)
            }
        
        # Max visibility side selection
        if left_elbow.visibility > right_elbow.visibility:
            hip_angle = self.calculate_angle(
                (left_shoulder.x, left_shoulder.y),
                (left_hip.x, left_hip.y),
                (left_ankle.x, left_ankle.y)
            )
            elbow_angle = self.calculate_angle(
                (left_shoulder.x, left_shoulder.y),
                (left_elbow.x, left_elbow.y),
                (left_wrist.x, left_wrist.y)
            )
        else:
            hip_angle = self.calculate_angle(
                (right_shoulder.x, right_shoulder.y),
                (right_hip.x, right_hip.y),
                (right_ankle.x, right_ankle.y)
            )
            elbow_angle = self.calculate_angle(
                (right_shoulder.x, right_shoulder.y),
                (right_elbow.x, right_elbow.y),
                (right_wrist.x, right_wrist.y)
            )
            
        # Target Plank Ranges:
        # Flat spine: 170 <= hip <= 186 degrees
        # Stacked elbow: 75 <= elbow <= 105 degrees
        is_flat_back = 170.0 <= hip_angle <= 186.0
        is_elbow_stacked = 70.0 <= elbow_angle <= 110.0
        
        current_time = time.time()
        
        if is_flat_back and is_elbow_stacked:
            self.stage = "holding"
            if self.plank_start_time is None:
                self.plank_start_time = current_time
                self.last_timer_tick = current_time
                self.feedback = "Form is perfect! Plank timer started."
            else:
                elapsed = current_time - self.last_timer_tick
                # Add only elapsed time to prevent timer jumps
                if elapsed > 0.0 and elapsed < 2.0:
                    self.hold_time += elapsed
                self.last_timer_tick = current_time
                
                # Increment 1 "rep" for every 5 seconds held
                calculated_reps = int(self.hold_time) // 5
                if calculated_reps > self.reps:
                    self.reps = calculated_reps
                    self.feedback = f"Excellent hold! {int(self.hold_time)}s achieved."
                else:
                    self.feedback = f"Keep holding! Core tight. {int(self.hold_time)}s..."
        else:
            self.stage = "setup"
            self.plank_start_time = None
            self.last_timer_tick = None
            
            if not is_flat_back:
                if hip_angle < 170.0:
                    self.feedback = "Form Warning: Engage your glutes! Don't let your hips sag."
                else:
                    self.feedback = "Form Warning: Hips too high! Lower your hips for a flat back."
            elif not is_elbow_stacked:
                self.feedback = "Form Warning: Adjust elbows directly below shoulders."
                
        return {
            "hip": hip_angle,
            "elbow": elbow_angle,
            "stability": "Optimal" if is_flat_back and is_elbow_stacked else "Sub-optimal",
            "duration": int(self.hold_time)
        }
