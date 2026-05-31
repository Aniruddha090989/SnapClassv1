import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students, 
    create_student_complete,  
    get_student_subjects, 
    get_student_attendance,
    unenroll_student_to_subject, 
    check_student_username_exists,  
    student_login_username_password,  
    get_student_by_voice,
    get_student_by_id  
)
import time
from src.components.dialog_enroll import enroll_dialog


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout", type='secondary', key='loginbackbtn'):
            st.session_state['is_logged_in'] = False
            st.session_state['student_login_method'] = None
            del st.session_state.student_data
            st.rerun()
    
    st.space()
    
    c1, c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch', key='enroll_btn'):
            enroll_dialog()
    
    st.divider()
    
    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)
    
    # Create detailed attendance view
    stats_map = {}
    detailed_attendance = []
    
    for log in logs:
        sid = log['subject_id']
        subject_name = log['subjects']['name'] if log.get('subjects') else f"Subject {sid}"
        
        if sid not in stats_map:
            stats_map[sid] = {
                "total": 0, 
                "attended": 0,
                "subject_name": subject_name,
                "subject_code": log['subjects']['subject_code'] if log.get('subjects') else "N/A",
                "attendance_records": []
            }
        
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1
        
        # Store detailed record
        stats_map[sid]['attendance_records'].append({
            "date": log['timestamp'][:10] if log.get('timestamp') else "Unknown",
            "time": log['timestamp'][11:19] if log.get('timestamp') else "Unknown",
            "status": "✅ Present" if log.get('is_present') else "❌ Absent"
        })
    
    # CSS to fix expander background
    st.markdown(
        """
        <style>
        /* Fix for Streamlit expander background */
        .stExpander {
            background-color: #f5f5f5 !important;
            border-radius: 10px !important;
        }
        .stExpander details {
            background-color: #f5f5f5 !important;
        }
        .stExpander summary {
            background-color: #e0e0e0 !important;
            color: #111111 !important;
            border-radius: 10px !important;
        }
        .stExpander summary:hover {
            background-color: #d0d0d0 !important;
        }
        div[data-testid="stExpander"] {
            background-color: #f5f5f5 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Display subjects in grid
    cols = st.columns(2)
    
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {"total": 0, "attended": 0, "subject_name": sub['name'], "subject_code": sub['subject_code']})
        
        # Calculate attendance percentage
        attendance_percentage = (stats['attended'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        def unenroll_button(sid=sid, sub_name=sub['name']):
            if st.button("🚪 Unenroll", type='secondary', width='stretch', key=f"unenroll_{sid}"):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f'Unenrolled from {sub_name} successfully!')
                st.rerun()
        
        with cols[i % 2]:
            # Subject card with detailed stats
            st.markdown(
                f"""
                <div style="background: white; border-left: 8px solid #EB459E; padding: 20px; border-radius: 15px; border: 1px solid #ddd; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h3 style="margin: 0 0 10px 0; color: #1e293b; font-size: 1.3rem;">📚 {sub['name']}</h3>
                    <p style="color: #64748b; margin: 5px 0;">
                        📖 Code: <span style="background: #E0E3FF; color: #5865F2; padding: 2px 8px; border-radius: 5px;">{sub['subject_code']}</span> 
                        | 📍 Section: {sub['section']}
                    </p>
                    <div style="background: #f0f0f0; border-radius: 10px; padding: 12px; margin: 12px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span>📊 Attendance Rate</span>
                            <span><b>{attendance_percentage:.1f}%</b></span>
                        </div>
                        <div style="background: #ddd; border-radius: 10px; overflow: hidden; height: 10px;">
                            <div style="background: #5865F2; width: {attendance_percentage}%; height: 10px;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <span>✅ Present: <b>{stats['attended']}</b></span>
                            <span>❌ Absent: <b>{stats['total'] - stats['attended']}</b></span>
                            <span>📅 Total: <b>{stats['total']}</b></span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # Unenroll button
            unenroll_button()
            
            # Expandable detailed attendance records
            with st.expander("📋 View Detailed Attendance Records"):
                if stats.get('attendance_records'):
                    for record in stats['attendance_records']:
                        st.markdown(
                            f"""
                            <div style="display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid #eee; background: white; color: #111111;">
                                <span>📅 {record['date']}</span>
                                <span>⏰ {record['time']}</span>
                                <span>{record['status']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No attendance records found for this subject.")
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    footer_dashboard()


def student_login_username_password():
    st.subheader("Login with Username & Password")
    
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
    
    with row1_col2:
        password = st.text_input("Password", placeholder="Enter your password", type="password", key="login_password")
    
    if st.button("🔐 Sign In", type='primary', width='stretch', key="login_btn"):
        if username and password:
            student = student_login_username_password(username, password)
            if student:
                st.session_state.is_logged_in = True
                st.session_state.user_role = 'student'
                st.session_state.student_data = student
                st.session_state.student_login_method = 'password'
                st.success(f'Welcome back {student["name"]}!')
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password!")
        else:
            st.warning("Please enter both username and password")


def student_login_face():
    st.subheader("Login with Face ID")
    st.write("Position your face at the center of the camera")
    
    photo_source = st.camera_input("Take a photo for face recognition", key="face_login_cam")
    
    if photo_source:
        img = np.array(Image.open(photo_source))
        
        with st.spinner('AI is scanning your face...'):
            detected, all_ids, num_faces = predict_attendance(img)
            
            if num_faces == 0:
                st.warning('No face detected! Please try again.')
            elif num_faces > 1:
                st.warning('Multiple faces detected! Please ensure only your face is visible.')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)
                    
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.session_state.student_login_method = 'face'
                        st.success(f'Welcome back {student["name"]}!')
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Face not recognized! Please register first.")
                else:
                    st.error("Face not recognized! Please register first.")


def student_login_voice():
    st.subheader("Login with Voice ID")
    st.write("Record a short phrase like 'I am present' or 'My name is [Your Name]'")
    
    audio_data = st.audio_input("Record your voice", key="voice_login_audio")
    
    if audio_data:
        with st.spinner('Analyzing your voice...'):
            audio_bytes = audio_data.read()
            voice_embedding = get_voice_embedding(audio_bytes)
            
            if voice_embedding:
                student = get_student_by_voice(voice_embedding)
                
                if student:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = 'student'
                    st.session_state.student_data = student
                    st.session_state.student_login_method = 'voice'
                    st.success(f'Welcome back {student["name"]}!')
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Voice not recognized! Please register first or try again.")
            else:
                st.error("Could not process voice. Please try again.")


def student_register():
    st.header("Register New Student Account")
    st.write("Create your account to start attending classes")
    
    with st.form("student_registration_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your full name", key="reg_name")
            username = st.text_input("Username *", placeholder="Choose a username", key="reg_username")
            password = st.text_input("Password *", type="password", placeholder="Create a password", key="reg_password")
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password", key="reg_confirm")
        
        with col2:
            st.write("**Face Enrollment (Required)**")
            face_photo = st.camera_input("Position your face at the center *", key="register_face_cam")
            
            st.write("**Voice Enrollment (Optional)**")
            voice_audio = st.audio_input("Record a short phrase like 'I am present'", key="register_voice_audio")
        
        submitted = st.form_submit_button("Register Now", type='primary', use_container_width=True)
        
        if submitted:
            errors = []
            
            if not name:
                errors.append("Full Name is required")
            if not username:
                errors.append("Username is required")
            if not password:
                errors.append("Password is required")
            if password != confirm_password:
                errors.append("Passwords do not match")
            if not face_photo:
                errors.append("Face photo is required")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                with st.spinner("Checking existing records..."):
                    # Check if username already exists
                    if check_student_username_exists(username):
                        st.error("❌ Username already registered! Please choose a different username.")
                    else:
                        img = np.array(Image.open(face_photo))
                        face_encodings = get_face_embeddings(img)
                        
                        if not face_encodings:
                            st.error("Could not detect face in the photo. Please try again with better lighting.")
                        else:
                            face_embedding = face_encodings[0].tolist()
                            
                            # Use predict_attendance to check if face already exists
                            detected, all_ids, num_faces = predict_attendance(img)
                            
                            if num_faces == 0:
                                st.warning('Face not found! Please try again.')
                            elif num_faces > 1:
                                st.warning('Multiple faces found! Please ensure only your face is visible.')
                            else:
                                if detected:
                                    # Face already registered
                                    student_id = list(detected.keys())[0]
                                    all_students = get_all_students()
                                    existing_student = next((s for s in all_students if s['student_id'] == student_id), None)
                                    
                                    if existing_student:
                                        
                                        st.error("❌ Face already registered! Please use existing account.")
                                else:
                                    # Face is new, proceed with registration
                                    with st.spinner("Creating your account..."):
                                        voice_embedding = None
                                        if voice_audio:
                                            voice_embedding = get_voice_embedding(voice_audio.read())
                                        
                                        response = create_student_complete(
                                            username=username,
                                            password=password,
                                            name=name,
                                            face_embedding=face_embedding,
                                            voice_embedding=voice_embedding
                                        )
                                        
                                        if response:
                                            train_classifier()
                                            st.success("Account created successfully! Please login.")
                                            time.sleep(2)
                                            st.session_state.student_login_option = 'face'
                                            st.rerun()
                                        else:
                                            st.error("Failed to create account. Please try again.")


def student_screen():
    style_base_layout()
    style_background_dashboard()
    
    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home', type='secondary', key='loginbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()
    
    st.space()
    st.space()
    
    if 'student_login_option' not in st.session_state:
        st.session_state.student_login_option = 'face'
    
    st.header("Student Login", text_alignment='center')

    


    
    
    
    col1, col2, col3, col4 = st.columns(4, gap='small')
    
    with col1:
        btn_type = "primary" if st.session_state.student_login_option == 'face' else "tertiary"
        if st.button('👤 Face ID', type=btn_type, width='stretch', key='tab_face'):
            st.session_state.student_login_option = 'face'
            st.rerun()
    
    with col2:
        btn_type = "primary" if st.session_state.student_login_option == 'password' else "tertiary"
        if st.button('🔐 Password', type=btn_type, width='stretch', key='tab_password'):
            st.session_state.student_login_option = 'password'
            st.rerun()
    
    with col3:
        btn_type = "primary" if st.session_state.student_login_option == 'voice' else "tertiary"
        if st.button('🎤 Voice', type=btn_type, width='stretch', key='tab_voice'):
            st.session_state.student_login_option = 'voice'
            st.rerun()
    
    with col4:
        btn_type = "primary" if st.session_state.student_login_option == 'register' else "secondary"
        if st.button('📝 Register', type=btn_type, width='stretch', key='tab_register'):
            st.session_state.student_login_option = 'register'
            st.rerun()
    
    st.divider()
    
    if st.session_state.student_login_option == 'face':
        student_login_face()
    elif st.session_state.student_login_option == 'password':
        student_login_username_password()
    elif st.session_state.student_login_option == 'voice':
        student_login_voice()
    elif st.session_state.student_login_option == 'register':
        student_register()
    
    footer_dashboard()
