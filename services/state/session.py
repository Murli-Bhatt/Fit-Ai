import streamlit as st
import datetime

def init_workout_session():
    """
    Initializes all workout-related session state variables with default values
    if they do not already exist. Handles edge cases where user changes tabs or reloads.
    """
    # Base states
    if 'workout_active' not in st.session_state:
        st.session_state.workout_active = False
    if 'active_exercise' not in st.session_state:
        st.session_state.active_exercise = "Squats"
    if 'target_sets' not in st.session_state:
        st.session_state.target_sets = 3
    if 'target_reps' not in st.session_state:
        st.session_state.target_reps = 10
    if 'current_set' not in st.session_state:
        st.session_state.current_set = 1
    if 'current_reps' not in st.session_state:
        st.session_state.current_reps = 0
    if 'voice_coaching' not in st.session_state:
        st.session_state.voice_coaching = True
    if 'feedback_cue' not in st.session_state:
        st.session_state.feedback_cue = "Ready to start! Maintain slow and controlled movements."
    if 'set_history' not in st.session_state:
        st.session_state.set_history = []
    
    # Persistent analytics logs
    if 'workout_logs' not in st.session_state:
        st.session_state.workout_logs = []

    # Dynamic joint angles simulation values
    if 'simulated_angles' not in st.session_state:
        st.session_state.simulated_angles = {
            # Squat values
            "squats": {"knee": 170.0, "hip": 170.0, "depth": "Standing", "back": "Neutral"},
            # Push-up values
            "push_ups": {"elbow": 175.0, "torso": 178.0, "depth": "Top Plank", "symmetry": "Balanced"},
            # Bicep Curl values
            "bicep_curls": {"elbow_l": 165.0, "elbow_r": 165.0, "stability": "High", "range": "Full Extension"},
            # Plank values
            "plank": {"hip": 178.0, "elbow": 90.0, "stability": "Optimal", "duration": 0},
            # Lunges values
            "lunges": {"front_knee": 170.0, "back_knee": 165.0, "torso": "Straight", "depth": "Standing"},
            # Shoulder Press values
            "shoulder_press": {"elbow_l": 95.0, "elbow_r": 95.0, "extension": "Low", "symmetry": "Balanced"}
        }

def start_workout_session(exercise, sets, reps, voice_coaching):
    """
    Transitions the application to an active workout session.
    Populates default history and clears progress.
    """
    init_workout_session()
    
    st.session_state.workout_active = True
    st.session_state.active_exercise = exercise
    st.session_state.target_sets = int(sets)
    st.session_state.target_reps = int(reps)
    st.session_state.current_set = 1
    st.session_state.current_reps = 0
    st.session_state.voice_coaching = voice_coaching
    st.session_state.feedback_cue = "Workout session started! Get into position."
    
    # Pre-populate empty set history table
    st.session_state.set_history = [
        {"set": s, "completed_reps": 0, "target_reps": int(reps), "status": "Pending"}
        for s in range(1, int(sets) + 1)
    ]
    st.session_state.set_history[0]["status"] = "Active"
    
    # Initialize simulation states to default standing/resting values based on exercise
    reset_simulated_angles()

def reset_simulated_angles():
    """
    Helper to reset joint angle configurations to starting values
    """
    if 'simulated_angles' in st.session_state:
        st.session_state.simulated_angles = {
            "squats": {"knee": 170.0, "hip": 170.0, "depth": "Standing", "back": "Neutral"},
            "push_ups": {"elbow": 175.0, "torso": 178.0, "depth": "Top Plank", "symmetry": "Balanced"},
            "bicep_curls": {"elbow_l": 165.0, "elbow_r": 165.0, "stability": "High", "range": "Full Extension"},
            "plank": {"hip": 178.0, "elbow": 90.0, "stability": "Optimal", "duration": 0},
            "lunges": {"front_knee": 170.0, "back_knee": 165.0, "torso": "Straight", "depth": "Standing"},
            "shoulder_press": {"elbow_l": 95.0, "elbow_r": 95.0, "extension": "Low", "symmetry": "Balanced"}
        }

def trigger_rep_success():
    """
    Adds a completed repetition to the active set, processes set completion,
    and handles global workout completion safely.
    """
    init_workout_session()
    
    if not st.session_state.workout_active:
        return
        
    curr_set_idx = st.session_state.current_set - 1
    
    # Safely guard indices
    if curr_set_idx >= len(st.session_state.set_history):
        return
        
    st.session_state.current_reps += 1
    st.session_state.set_history[curr_set_idx]["completed_reps"] = st.session_state.current_reps
    
    # Check if active set target is reached
    if st.session_state.current_reps >= st.session_state.target_reps:
        st.session_state.set_history[curr_set_idx]["status"] = "Completed"
        
        # Check if more sets are remaining
        if st.session_state.current_set < st.session_state.target_sets:
            st.session_state.current_set += 1
            st.session_state.current_reps = 0
            st.session_state.set_history[st.session_state.current_set - 1]["status"] = "Active"
            st.session_state.feedback_cue = f"Set {st.session_state.current_set - 1} completed! Breathe and start Set {st.session_state.current_set}."
        else:
            # Entire workout completed!
            finish_workout_session(completed_successfully=True)
    else:
        st.session_state.feedback_cue = f"Good rep! {st.session_state.current_reps}/{st.session_state.target_reps} completed in Set {st.session_state.current_set}."

def finish_workout_session(completed_successfully=True):
    """
    Concludes the current workout. Saves the stats inside the user's workout logs,
    and returns state to config mode.
    """
    init_workout_session()
    
    if not st.session_state.workout_active:
        return
        
    # Calculate total reps completed
    total_reps = sum(s["completed_reps"] for s in st.session_state.set_history)
    
    # Save log
    if total_reps > 0:
        new_log = {
            "username": st.session_state.get("username", "gymcoach"),
            "exercise": st.session_state.active_exercise,
            "reps": total_reps,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.workout_logs.append(new_log)
        
    # Reset active state
    st.session_state.workout_active = False
    
    if completed_successfully:
        st.session_state.feedback_cue = f"Session complete! You finished a total of {total_reps} reps of {st.session_state.active_exercise}."
    else:
        st.session_state.feedback_cue = f"Session stopped. Completed {total_reps} reps total."

def stop_workout_session():
    """
    User clicks stop: Cancel the workout, save whatever reps they did, and return to configurator.
    """
    finish_workout_session(completed_successfully=False)
