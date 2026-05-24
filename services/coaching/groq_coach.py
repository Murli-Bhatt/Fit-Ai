import os
import time
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from services.coaching.text_to_speech import text_to_speech_base64

# Resolve absolute path to project root .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

# Safe API key retrieval (checks environment variables, then falls back to Streamlit secrets)
API_KEY = os.getenv("groq_api_key") or os.getenv("GROQ_API_KEY")
if not API_KEY:
    try:
        API_KEY = st.secrets.get("groq_api_key") or st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

SYSTEM_PROMPT = """
You are FIT-AI, an elite, highly encouraging personal AI Gym Trainer.
The user just completed a repetition. Keep your coaching advice extremely brief, highly actionable, motivating, and conversational (MAXIMUM 15 words).

You will be given:
1. Intended Exercise: The exercise the user chose.
2. Repetition State: Just completed Rep X of Y (Set A of B).
3. Rep Performance Assessment: A list of biomechanical issues/warnings observed during this rep (or 'None' if it was a perfect rep).

Your core coaching logic:
- If 'Rep Performance Assessment' is 'None', congratulate them on a perfect, clean repetition and give them a quick motivational push (e.g., 'Perfect depth on that squat! Squeeze and keep going!').
- If 'Rep Performance Assessment' contains posture errors (e.g., 'leaning forward', 'elbow flare', 'hips sagging'), give a quick, constructive correction for their next rep (e.g., 'You leaned forward on that last rep. Squeeze your core and keep chest high on the next one!').
- If they completed the entire set, congratulate them and tell them to rest.
- Never mention landmarks, coordinates, angles, code variables, or that you are an AI. 
- Talk naturally as if you are standing right next to them in the gym. Speak in one concise sentence!
"""

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
    Queries Groq's Llama 3.1 model to generate instant, context-aware training guidance upon rep completion.
    """
    if not API_KEY:
        # Fallback to the original CV rule-based feedback cue if API key is not configured
        errors_str = ", ".join(set(rep_errors)) if rep_errors else "Excellent form!"
        return f"Rep completed. Errors: {errors_str}"

    try:
        client = Groq(api_key=API_KEY)
        
        # Prepare context payload for the model
        errors_str = ", ".join(set(rep_errors)) if rep_errors else "None (Perfect form!)"
        user_message = (
            f"Intended Exercise: {exercise_name}\n"
            f"Repetition State: Completed Rep {current_reps} of {target_reps} (Set {current_set} of {target_sets})\n"
            f"Rep Performance Assessment: {errors_str}\n"
            f"Joint Angles/Status: {angles_dict}\n"
        )
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.1-8b-instant",
            max_tokens=40,
            temperature=0.7,
        )
        
        coaching_text = response.choices[0].message.content.strip()
        
        # Strip outer quotes if the model wrapped the response in quotes
        if coaching_text.startswith('"') and coaching_text.endswith('"'):
            coaching_text = coaching_text[1:-1].strip()
            
        return coaching_text
        
    except Exception as e:
        # Fallback to CV rule feedback if API fails or rate-limits
        print(f"Groq API Error: {str(e)}")
        errors_str = ", ".join(set(rep_errors)) if rep_errors else "Excellent form!"
        return f"Rep completed. Errors: {errors_str}"

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
            
            # Convert to TTS (Base64)
            audio_b64 = text_to_speech_base64(coaching_text)
            return audio_b64
            
    return ""
