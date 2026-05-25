import streamlit as st

def render_progress_metric(set_history, current_set, current_reps, target_reps):
    """
    Renders an outstanding, glassmorphic progress card directly inside the Streamlit sidebar,
    displaying total completed repetitions and the active set's details.
    """
    # Calculate total reps completed in the entire session
    total_reps = sum(s["completed_reps"] for s in set_history)
    total_sets = len(set_history)
    
    # Calculate progress percentage of active set
    progress_percentage = min(100, int((current_reps / target_reps) * 100)) if target_reps > 0 else 0
    
    # Compile glassmorphic HTML card
    progress_html = f"""
    <div class="stat-card" style="margin-bottom: 20px; border-color: rgba(0, 255, 204, 0.2); background: rgba(255, 255, 255, 0.03);">
        <div style="font-size: 0.75rem; color: #00FFCC; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📈 Workout Progress</div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div>
                <div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600;">Total Reps</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; line-height: 1; margin-top: 3px;">{total_reps}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600;">Set {current_set} of {total_sets}</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #00FFCC; line-height: 1; margin-top: 3px;">
                    {current_reps} <span style="font-size: 0.85rem; color: #9ca3af; font-weight: 400;">/ {target_reps} reps</span>
                </div>
            </div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.05); height: 8px; border-radius: 4px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="background: linear-gradient(90deg, #00FFCC 0%, #0099FF 100%); width: {progress_percentage}%; height: 100%; border-radius: 4px; transition: width 0.4s ease-in-out;"></div>
        </div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)
