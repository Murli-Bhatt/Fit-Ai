import os
import time
import streamlit as st
from dotenv import load_dotenv
from services.coaching.text_to_speech import text_to_speech_base64

# Resolve absolute path to project root .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

# local rule-based caching config
def query_groq_coach(
    exercise_name: str,
    current_set: int,
    current_reps: int,
    target_sets: int,
    target_reps: int,
    rep_errors: list,
    angles_dict: dict
) -> str:
    """
    Local rule-based coach feedback generator.
    Replaces Groq API to provide instant, zero-latency, context-aware training guidance.
    """
    # Clean unique errors
    unique_errors = list(set([e.strip() for e in rep_errors if e and e.strip()]))
    errors_lower = [e.lower() for e in unique_errors]
    
    # 1. Workout / Set Completion logic
    if current_reps >= target_reps:
        if current_set >= target_sets:
            extra_cues = [
                "Target reached! Outstanding effort! Let's push for one extra bonus rep!",
                "Goal achieved! Phenomenal strength! Show off and do one more pushup!",
                "Target completed! Brilliant! Keep the momentum and do an extra repetition!",
                "Target hit! Spectacular! Keep going, show your ultimate limits!",
                "Target met! Unstoppable! Let's do another rep for good measure!"
            ]
            idx = current_reps % len(extra_cues)
            return extra_cues[idx]
        else:
            return f"Set {current_set} completed! Awesome job. Take a quick rest, then get ready for set {current_set + 1}."
            
    # 2. Form Correction Logic (If there are errors)
    if unique_errors:
        err_str = " ".join(errors_lower)
        ex_lower = exercise_name.lower()
        
        # SQUATS
        if "squat" in ex_lower:
            if any(word in err_str for word in ["lean", "leaning", "forward"]):
                return "Keep your chest proud and high on the next squat. Don't lean forward!"
            elif any(word in err_str for word in ["depth", "deep", "low", "standing"]):
                return "Go a bit lower on the next rep to get full depth and engage your glutes!"
            elif any(word in err_str for word in ["knee", "cave", "inward"]):
                return "Push your knees slightly outward as you squat down!"
            else:
                return "Slow down, stabilize your core, and check your squat form."
                
        # PUSH-UPS
        elif "push" in ex_lower:
            if any(word in err_str for word in ["sag", "hips", "low", "belly"]):
                return "Squeeze your glutes and core! Keep your hips in a straight line on the next rep."
            elif any(word in err_str for word in ["depth", "low", "chest"]):
                return "Lower your chest a bit closer to the floor on the next push-up!"
            elif any(word in err_str for word in ["elbow", "flare", "wide"]):
                return "Keep your elbows tucked at a forty-five degree angle!"
            else:
                return "Engage your core, keep your body straight, and push up strong!"
                
        # BICEP CURLS
        elif "bicep" in ex_lower or "curl" in ex_lower:
            if any(word in err_str for word in ["swing", "momentum", "flare", "stability", "arm"]):
                return "Lock your elbows to your sides! Avoid swinging your arms to lift the weight."
            elif any(word in err_str for word in ["range", "partial", "stretch", "extension"]):
                return "Ensure full range of motion. Lower the weight all the way down!"
            else:
                return "Squeeze your biceps hard at the peak, then control the descent!"
                
        # PLANK
        elif "plank" in ex_lower:
            if any(word in err_str for word in ["sag", "low", "hip", "hips"]):
                return "Squeeze your abs and raise your hips slightly! Don't let them sag."
            elif any(word in err_str for word in ["raise", "high", "pike"]):
                return "Lower your hips to a perfectly flat, neutral alignment."
            else:
                return "Keep your neck relaxed, press through your elbows, and hold strong!"
                
        # LUNGES
        elif "lunge" in ex_lower:
            if any(word in err_str for word in ["knee", "front", "cave", "wobble"]):
                return "Keep your front knee aligned over your ankle. Don't let it wobble!"
            elif any(word in err_str for word in ["torso", "lean", "upright"]):
                return "Keep your chest up and shoulders back on the next step!"
            else:
                return "Drop your hips straight down and push off your front heel!"
                
        # SHOULDER PRESS
        elif "shoulder" in ex_lower or "press" in ex_lower:
            if any(word in err_str for word in ["flare", "elbow", "wide"]):
                return "Keep your elbows slightly forward to protect your shoulders!"
            elif any(word in err_str for word in ["extension", "range", "short"]):
                return "Press the weight all the way up to full elbow extension!"
            else:
                return "Control the weights as you lower them and press straight up!"
                
        # GENERAL FALLBACK FOR ERRORS
        else:
            first_err = unique_errors[0].replace("Warning:", "").replace("Form Warning:", "").strip()
            return f"Watch your form on the next rep: {first_err}."

    # 3. Motivational Perfect Rep Logic (If form was clean!)
    perfect_cues = [
        f"Perfect form on rep {current_reps}! Keep that exact motion going.",
        f"Clean rep {current_reps}! Brilliant control, keep it up.",
        "Spot on! Your joint alignment is absolutely beautiful.",
        "Excellent pace! Squeeze at the peak and continue.",
        "Beautiful rep! Stay focused and drive through.",
        f"Rep {current_reps} solid! Keep pushing through this set!"
    ]
    
    # Deterministic selection based on rep count
    cue_idx = current_reps % len(perfect_cues)
    return perfect_cues[cue_idx]

def speak_text_locally(text: str):
    """
    Synthesizes and speaks text directly on the local machine speakers using the Windows native PowerShell System.Speech API.
    Runs asynchronously in a detached subprocess to prevent UI freezing, and is 100% immune to browser/Streamlit lifecycle events.
    """
    import subprocess
    # Escape single quotes and double quotes safely for PowerShell compatibility
    safe_text = text.replace("'", "''").replace('"', '\\"')
    cmd = [
        "powershell",
        "-Command",
        f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{safe_text}')"
    ]
    try:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Local text-to-speech engine failed: {str(e)}")

def trigger_coaching_audio(
    exercise_name: str,
    current_set: int,
    current_reps: int,
    target_sets: int,
    target_reps: int,
    rep_errors: list,
    angles_dict: dict,
    force: bool = False
) -> str:
    """
    Orchestrates the voice coaching feedback upon rep completion. Checks rate-limits and state transitions 
    to decide if we should speak. If yes, it queries Groq, converts to TTS, and returns 
    the base64 encoded audio string to be played in the browser.
    
    Returns:
        str: Base64 audio payload or empty string if no speech is triggered.
    """
    # 1. Safely check voice_coaching toggle
    if not st.session_state.get("voice_coaching", True):
        return ""

    current_time = time.time()
    should_speak = False
    
    # 2. Condition A: A new set is completed (or started)
    if current_set != st.session_state.get("last_spoken_set", 0):
        st.session_state.last_spoken_set = current_set
        st.session_state.last_spoken_rep = current_reps # Align rep counters
        should_speak = True
        
    # 3. Condition B: A new rep is completed
    elif current_reps != st.session_state.get("last_spoken_rep", 0):
        st.session_state.last_spoken_rep = current_reps
        should_speak = True
        
    # 4. Condition C: Force trigger
    elif force:
        should_speak = True

    # 5. If we should speak, run the pipeline
    if should_speak:
        # Update last spoken time
        st.session_state.last_spoken_time = current_time
        
        # Query Groq
        coaching_text = query_groq_coach(
            exercise_name=exercise_name,
            current_set=current_set,
            current_reps=current_reps,
            target_sets=target_sets,
            target_reps=target_reps,
            rep_errors=rep_errors,
            angles_dict=angles_dict
        )
        
        if coaching_text:
            # Update session feedback cue if we got a new one to display on the Streamlit UI!
            st.session_state.feedback_cue = coaching_text
            
            # Speak natively through local system audio (100% immune to Streamlit DOM updates/reruns!)
            speak_text_locally(coaching_text)
            
            # Convert to TTS (Base64)
            audio_b64 = text_to_speech_base64(coaching_text)
            return audio_b64
            
    return ""
