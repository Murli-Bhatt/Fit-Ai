import streamlit as st

def render_shoulder_press_metrics(angles):
    """
    Renders visual indicators and posture logs specific to Overhead Shoulder Press.
    """
    elbow_l = angles.get("elbow_l", 95.0)
    elbow_r = angles.get("elbow_r", 95.0)
    
    # Calculate symmetry (difference between left and right extension)
    diff = abs(elbow_l - elbow_r)
    if diff <= 12:
        symmetry = "Excellent Arm Symmetry (Balanced)"
        sym_color = "#00FFCC"
    elif diff <= 25:
        symmetry = "Slight Asymmetric Push (Stabilize)"
        sym_color = "#FFA500"
    else:
        symmetry = "Highly Uneven Press! (Symmetric posture required)"
        sym_color = "#FF3366"

    # Analyze extension depth
    avg_extension = (elbow_l + elbow_r) / 2.0
    if avg_extension >= 155:
        extension_status = "Full Overhead Extension (Locked Out)"
        ext_color = "#00FFCC"
    elif avg_extension >= 110:
        extension_status = "Mid Range (Push higher!)"
        ext_color = "#0099FF"
    elif avg_extension <= 75:
        extension_status = "Excellent Starting Depth (Bottom Stack)"
        ext_color = "#00FFCC"
    else:
        extension_status = "Partial Range / Incomplete Drive"
        ext_color = "#FFA500"

    st.markdown("<h4 style='color: #00FFCC; font-weight: 600; margin-bottom: 12px;'>🏋️‍♂️ Shoulder Press Biometrics</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Left Elbow</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{elbow_l:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #00FFCC; width: {min(100, int((elbow_l/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Top target: ≥ 160° lockout</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Right Elbow</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{elbow_r:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #0099FF; width: {min(100, int((elbow_r/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Top target: ≥ 160° lockout</div>
        </div>
        """, unsafe_allow_html=True)

    # Posture alerts
    st.markdown(f"""
    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {ext_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Overhead Drive Extension</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{extension_status}</div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {sym_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Arm Symmetry Analysis</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{symmetry}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
