import streamlit as st

def render_bicep_curl_metrics(angles):
    """
    Renders visual indicators and alignment logs specific to Bicep Curls.
    """
    elbow_l = angles.get("elbow_l", 165.0)
    elbow_r = angles.get("elbow_r", 165.0)
    
    # Calculate contraction state based on minimum angle between left and right arms
    min_angle = min(elbow_l, elbow_r)
    max_angle = max(elbow_l, elbow_r)
    
    if min_angle <= 50:
        range_status = "Full Peak Contraction (Excellent)"
        range_color = "#00FFCC"
    elif min_angle <= 90:
        range_status = "Squeeze Your Biceps More"
        range_color = "#0099FF"
    elif max_angle >= 150:
        range_status = "Full Stretch / Extension"
        range_color = "#00FFCC"
    else:
        range_status = "Mid Range / Partial Rep"
        range_color = "#FFA500"

    stability = angles.get("stability", "High")
    if stability == "High":
        stab_status = "Arms Locked (Perfect Upper Arm Stability)"
        stab_color = "#00FFCC"
    elif stability == "Medium":
        stab_status = "Slight Flare / Swing Detected"
        stab_color = "#FFA500"
    else:
        stab_status = "Excessive Elbow Swing / Using Momentum!"
        stab_color = "#FF3366"

    st.markdown("<h4 style='color: #00FFCC; font-weight: 600; margin-bottom: 12px;'>💪 Bicep Curl Biometrics</h4>", unsafe_allow_html=True)
    
    # Grid of gauges
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Left Elbow</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{elbow_l:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #00FFCC; width: {min(100, int((elbow_l/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Contraction target: ≤ 40°</div>
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
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Contraction target: ≤ 40°</div>
        </div>
        """, unsafe_allow_html=True)

    # Posture alerts
    st.markdown(f"""
    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {range_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Range of Motion</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{range_status}</div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {stab_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Arm Stability</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{stab_status}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
