from src.database.config import supabase
import bcrypt
import numpy as np


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_password(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username, password, name):
    data = {"username": username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_password(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data


def create_student(new_name, face_embedding=None, voice_embedding=None):
    """Create student with name and optional face/voice embeddings"""
    data = {'name': new_name, 'face_embedding': face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_student_complete(username, password, name, face_embedding=None, voice_embedding=None):
    """Create student with username, password, name, and optional face/voice"""
    data = {
        'username': username,
        'password': hash_pass(password),
        'name': name,
        'face_embedding': face_embedding,
        'voice_embedding': voice_embedding
    }
    response = supabase.table('students').insert(data).execute()
    return response.data


def student_login_username_password(username, password):
    """Login using username and password"""
    response = supabase.table('students').select("*").eq("username", username).execute()
    if response.data:
        student = response.data[0]
        if check_password(password, student['password']):
            return student
    return None


def get_student_by_voice(voice_embedding, threshold=0.65):
    """Find student by voice embedding"""
    all_students = get_all_students()
    
    if not all_students:
        return None
    
    best_match = None
    best_score = -1.0
    
    for student in all_students:
        stored_embedding = student.get('voice_embedding')
        if stored_embedding:
            if isinstance(stored_embedding, list):
                stored_embedding = np.array(stored_embedding)
            if isinstance(voice_embedding, list):
                voice_embedding = np.array(voice_embedding)
            
            similarity = np.dot(voice_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_match = student
    
    if best_score >= threshold:
        return best_match
    return None


def check_student_username_exists(username):
    """Check if username already exists"""
    response = supabase.table('students').select("username").eq("username", username).execute()
    return len(response.data) > 0


def check_student_exists(username):
    """Alias for check_student_username_exists"""
    return check_student_username_exists(username)


def get_student_by_id(student_id):
    """Get student by ID"""
    response = supabase.table('students').select("*").eq("student_id", student_id).execute()
    if response.data:
        return response.data[0]
    return None


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data


def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attendance(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data
    
    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions
    
    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response = supabase.table('subject_students').insert(data).execute()
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data


def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table('attendance').insert(logs).execute()
    return response.data


def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data


def update_student_voice_embedding(student_id, voice_embedding):
    """Update voice embedding for existing student"""
    response = supabase.table('students').update({'voice_embedding': voice_embedding}).eq('student_id', student_id).execute()
    return response.data


def update_student_face_embedding(student_id, face_embedding):
    """Update face embedding for existing student"""
    response = supabase.table('students').update({'face_embedding': face_embedding}).eq('student_id', student_id).execute()
    return response.data
