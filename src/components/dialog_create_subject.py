import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    # Add CSS to fix visibility in dialog
    st.markdown("""
    <style>
    /* Dialog background and text visibility */
    div[role="dialog"] {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }
    
    div[role="dialog"] h1, 
    div[role="dialog"] h2, 
    div[role="dialog"] h3,
    div[role="dialog"] p,
    div[role="dialog"] label {
        color: black !important;
    }
    
    /* Input fields in dialog */
    div[role="dialog"] .stTextInput input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #5865F2 !important;
        border-radius: 0.5rem !important;
    }
    
    div[role="dialog"] .stTextInput input::placeholder {
        color: #999 !important;
    }
    
    /* Buttons in dialog */
    div[role="dialog"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.write("Enter the details of new subject")
    
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")
    
    if st.button("Create Subject Now", type='primary', width='stretch'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.success("Subject Created Successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all the fields")