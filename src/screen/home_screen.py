import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_dashboard, style_background_home
from src.components.footer import footer_home


def home_screen():
    
    # Add ADLaM Display font for headers and larger text for buttons
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=ADLaM+Display&display=swap');
    
    .adlam-header {
        font-family: 'ADLaM Display', cursive !important;
        font-size: 2rem !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }
    
    /* Make button text larger */
    .stButton button {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        padding: 12px 24px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    header_home()
    
    style_base_layout()
    style_background_dashboard()
    style_background_home()
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<h2 class="adlam-header">I\'m Teacher</h2>', unsafe_allow_html=True)
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
    
    with col2:
        st.markdown('<h2 class="adlam-header">I\'m Student</h2>', unsafe_allow_html=True)
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()
    
    footer_home()