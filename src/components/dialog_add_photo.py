import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image
import time


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    # Make all text white in the dialog
    st.markdown(
        """
        <style>
        /* Make dialog background dark */
        div[role="dialog"] {
            background-color: #1e1e1e !important;
        }
        
        /* Make ALL text inside dialog white */
        div[role="dialog"],
        div[role="dialog"] * {
            color: white !important;
        }
        
        /* File uploader dropzone background */
        section[data-testid="stFileUploaderDropzone"] {
            background-color: #2d2d2d !important;
        }
        
        /* Keep button colors as original */
        div[role="dialog"] button[kind="primary"] {
            background-color: #5865F2 !important;
            color: white !important;
        }
        
        div[role="dialog"] button[kind="tertiary"] {
            background-color: #EB459E !important;
            color: white !important;
        }
        
        /* Make dropdown arrows white */
        div[role="dialog"] svg {
            fill: white !important;
            color: white !important;
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