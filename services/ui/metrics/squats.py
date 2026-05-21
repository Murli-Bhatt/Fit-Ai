import streamlit as st

def render_squat_metrics(angles):
    """
    Renders visual indicators and alignment logs specific to Squats.
    """
    knee = angles.get("knee", 170.0)
    hip = angles.get("hip", 170.0)
    
    # Calculate depth status based on knee angle
    if knee <= 95:
        depth = "Deep Squat (Excellent)"
        depth_color = "#00FFCC"
    elif knee <= 110:
        depth = "Parallel (Good)"
        depth_color = "#0099FF"
    elif knee <= 140:
        depth = "Half Squat (Go Deeper)"
        depth_color = "#FFA500"
    else:
        depth = "Standing / Setup"
        depth_color = "#9ca3af"

    # Calculate back alignment based on hip angle vs knee angle
    # If the hip angle is significantly lower than knee angle or torso leans too far forward
    hip_knee_diff = hip - knee
    if hip_knee_diff < -20:
        back = "Leaning Forward (Keep Spine Straight)"
        back_color = "#FF3366"
    else:
        back = "Neutral Spine (Optimal)"
        back_color = "#00FFCC"

    st.markdown("<h4 style='color: #00FFCC; font-weight: 600; margin-bottom: 12px;'>🏋️‍♂️ Squat Biometrics</h4>", unsafe_allow_html=True)
    
    # Grid of gauges
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Knee Angle</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{knee:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #00FFCC; width: {min(100, int((knee/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Target: ≤ 90° for deep squat</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Hip Angle</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{hip:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #0099FF; width: {min(100, int((hip/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Syncs with depth flexion</div>
        </div>
        """, unsafe_allow_html=True)

    # Posture alerts
    st.markdown(f"""
    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {depth_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Depth Flexion</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{depth}</div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {back_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Spine Alignment</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{back}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
