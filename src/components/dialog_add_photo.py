import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image
import time


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    # Style the dialog and make all elements visible
    st.markdown(
        """
        <style>
        /* Dialog background */
        div[role="dialog"] {
            background-color: #f5f5dc !important;
        }
        
        /* Make the entire file uploader dropzone off-white */
        section[data-testid="stFileUploaderDropzone"] {
            background-color: #f5f5dc !important;
        }
        
        /* Make all text inside file uploader black */
        section[data-testid="stFileUploaderDropzone"] * {
            color: black !important;
        }
        
        /* Make dropdown arrow icons visible */
        div[role="dialog"] svg.icon,
        div[role="dialog"] svg[data-testid="stIcon"],
        div[role="dialog"] .stSelectbox svg {
            fill: black !important;
            color: black !important;
            stroke: black !important;
        }
        
        /* Make any arrow/chevron icons black */
        div[role="dialog"] svg {
            fill: black !important;
            color: black !important;
        }
        
        /* Keep upload button with light background */
        section[data-testid="stFileUploaderDropzone"] button {
            background-color: #e0e0e0 !important;
            color: black !important;
        }
        
        /* Keep Camera/Upload/Done button colors as before */
        div[role="dialog"] button[kind="primary"] {
            background-color: #5865F2 !important;
            color: white !important;
        }
        
        div[role="dialog"] button[kind="tertiary"] {
            background-color: #EB459E !important;
            color: white !important;
        }
        
        /* Make select box trigger visible */
        div[role="dialog"] .stSelectbox [data-baseweb="select"] {
            background-color: white !important;
        }
        
        div[role="dialog"] .stSelectbox [data-baseweb="select"] svg {
            fill: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.write('Add classroom photos to scan for attendance')

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('Photo Captured')
            st.rerun()

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader('choose image files', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key='dialog_upload')
        st.divider()
        if st.button('Done', type='primary', width='stretch'):
            if uploaded_files:
                for f in uploaded_files:
                    st.session_state.attendance_images.append(Image.open(f))
            st.toast('Photo Uploaded Successfully')
            st.rerun()