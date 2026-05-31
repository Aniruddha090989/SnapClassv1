import streamlit as st


def style_background_home():
    st.markdown(
        """
        <style>
        /* Force home page background */
        .stApp {
            background-color: #B6CEB4 !important;
            background: #B6CEB4 !important;
        }
        
        /* Override any other backgrounds */
        .stApp > header {
            background-color: #B6CEB4 !important;
        }
        
        .stApp div[data-testid="stColumn"] {
            background-color: #E0E3FF !important;
            padding: 2.5rem !important;
            border-radius: 5rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_background_dashboard():
    st.markdown(
        """
        <style>
        /* Main app background - slightly darker */
        .stApp {
            background: #E8EAF6 !important;
        }
        
        /* All text dark for readability */
        h1, h2, h3, h4, p, div, span, label {
            color: #111111 !important;
        }
        
        /* Input fields - white background, dark text */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {
            background-color: #FFFFFF !important;
            color: #111111 !important;
            border: 1px solid #5865F2 !important;
            border-radius: 0.5rem !important;
            padding: 0.5rem !important;
        }
        
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #666666 !important;
        }
        
        /* Dropdowns / select boxes - make text dark and arrow visible */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #111111 !important;
        }
        
        .stSelectbox div[data-baseweb="select"] span {
            color: #111111 !important;
        }
        
        /* Make dropdown arrow/icon visible */
        .stSelectbox svg {
            fill: #111111 !important;
            color: #111111 !important;
            stroke: #111111 !important;
        }
        
        /* Dropdown menu options */
        div[data-baseweb="popover"] ul {
            background-color: #FFFFFF !important;
        }
        
        div[data-baseweb="popover"] li {
            color: #111111 !important;
            background-color: #FFFFFF !important;
        }
        
        div[data-baseweb="popover"] li:hover {
            background-color: #D0D3F0 !important;
        }
        
        /* File uploader - uploaded file names */
        .stFileUploader [data-testid="stFileUploaderFile"] {
            color: #111111 !important;
            background-color: #F5F5F5 !important;
        }
        
        .stFileUploader [data-testid="stFileUploaderFile"] span {
            color: #111111 !important;
        }
        
        .stFileUploader label, .stFileUploader span, .stFileUploader div {
            color: #111111 !important;
        }
        
        .stFileUploader div[data-testid="stFileUploaderDropzone"] {
            background-color: #F5F5F5 !important;
            border: 1px solid #5865F2 !important;
        }
        
        /* Camera and audio input labels */
        .stCameraInput label, .stAudioInput label {
            color: #111111 !important;
        }
        
        /* Dataframes */
        .stDataFrame {
            background-color: #FFFFFF !important;
        }
        
        /* Divider */
        hr {
            border-color: #5865F2 !important;
            border-width: 2px !important;
            margin: 1rem 0 !important;
        }
        
        /* Make all SVG icons visible in select boxes */
        .stSelectbox [data-baseweb="select"] svg {
            fill: #111111 !important;
            color: #111111 !important;
        }
        
        /* Toast notifications - white background with dark text */
        .stToast {
            background-color: #FFFFFF !important;
            border-left: 4px solid #5865F2 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }
        
        .stToast * {
            color: #111111 !important;
        }
        
        .stToast svg {
            fill: #111111 !important;
            color: #111111 !important;
        }
        
        /* Keep button colors as they were */
        button {
            border-radius: 1.5rem !important;
            background-color: #5865F2 !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }
        
        button[kind="secondary"] {
            background-color: #EB459E !important;
            color: white !important;
        }
        
        button[kind="tertiary"] {
            background-color: white !important;
            color: #5865F2 !important;
            border: 1px solid #5865F2 !important;
        }
        
        button:hover {
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
        
        /* Hide Streamlit default menu and footer */
        MainMenu, footer, header {
            visibility: hidden;
        }
        
        .block-container {
            padding-top: 1.5rem !important;
        }
        
        h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
        }
        
        h2 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2rem !important;
            line-height: 0.9 !important;
            margin-bottom: 0rem !important;
            color: #111111 !important;
        }
        
        h3, h4, p {
            font-family: 'Outfit', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )