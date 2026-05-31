import streamlit as st


def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=ADLaM+Display&display=swap');
    
    .snapclass-title {{
        font-family: 'ADLaM Display', cursive !important;
        text-align: center;
        color: #E0E3FF;
        font-size: 2.5rem;
        margin: 0;
        line-height: 1.2;
        white-space: nowrap;
    }}
    </style>
    
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px">
        <img src='{logo_url}' style='height:100px;' />
        <h1 class='snapclass-title'>ATTENDIFY</h1>
    </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=ADLaM+Display&display=swap');
    
    .snapclass-dashboard-title {{
        font-family: 'ADLaM Display', cursive !important;
        text-align: left;
        color: #5865F2;
        font-size: 1.8rem;
        margin: 0;
        white-space: nowrap;
    }}
    </style>
    
    <div style="display:flex; align-items:center; justify-content:center; gap:10px">
        <img src='{logo_url}' style='height:65px;' />
        <h2 class='snapclass-dashboard-title'>ATTENDIFY</h2>
    </div>
    """, unsafe_allow_html=True)
