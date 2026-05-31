from src.database.config import supabase
import bcrypt


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
    data = {'name': new_name, 'face_embedding': face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


# ========== NEW FUNCTIONS FOR STUDENT AUTHENTICATION ==========

def check_student_exists(username):
    """Check if a student with given username already exists"""
    response = supabase.table("students").select("username").eq("username", username).execute()
    return len(response.data) > 0


def check_face_exists(face_embedding, threshold=0.6):
    """Check if a face embedding already exists in the database"""
    response = supabase.table("students").select("student_id, name, face_embedding").not_.is_("face_embedding", "null").execute()
    
    if not response.data:
        return None
    
    import numpy as np
    for student in response.data:
        stored_embedding = student.get('face_embedding')
        if stored_embedding:
            # Calculate similarity
            similarity = np.dot(face_embedding, stored_embedding)
            if similarity > threshold:
                return student  # Return the existing student
    return None


def create_student_with_auth(name, username, password, face_embedding=None, voice_embedding=None):
    """Create a new student with username, password, face embedding, and optional voice embedding"""
    data = {
        'name': name,
        'username': username,
        'password': hash_pass(password),
        'face_embedding': face_embedding,
        'voice_embedding': voice_embedding
    }
    response = supabase.table('students').insert(data).execute()
    return response.data


def student_login_password(username, password):
    """Login student using username and password"""
    response = supabase.table("students").select("*").eq("username", username).execute()
    if response.data:
        student = response.data[0]
        if student.get('password') and check_password(password, student['password']):
            return student
    return None


def get_student_by_face(face_embedding):
    """Find student by face embedding (compare with stored embeddings)"""
    # Get all students with face embeddings
    response = supabase.table("students").select("*").not_.is_("face_embedding", "null").execute()
    
    if not response.data:
        return None
    
    # Simple comparison - in production, use proper vector similarity
    import numpy as np
    best_match = None
    best_score = -1
    
    for student in response.data:
        stored_embedding = student.get('face_embedding')
        if stored_embedding:
            # Calculate cosine similarity or Euclidean distance
            similarity = np.dot(face_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_match = student
    
    # Threshold for face matching (adjust as needed)
    if best_score > 0.6:
        return best_match
    return None


def get_student_by_voice(voice_embedding, threshold=0.65):
    """Find student by voice embedding"""
    # Get all students with voice embeddings
    response = supabase.table("students").select("*").not_.is_("voice_embedding", "null").execute()
    
    if not response.data:
        return None
    
    # Simple comparison - in production, use proper vector similarity
    import numpy as np
    best_match = None
    best_score = -1
    
    for student in response.data:
        stored_embedding = student.get('voice_embedding')
        if stored_embedding:
            similarity = np.dot(voice_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_match = student
    
    if best_score >= threshold:
        return best_match
    return None


def update_student_face_embedding(student_id, face_embedding):
    """Update a student's face embedding"""
    response = supabase.table('students').update({'face_embedding': face_embedding}).eq('student_id', student_id).execute()
    return response.data


def update_student_voice_embedding(student_id, voice_embedding):
    """Update a student's voice embedding"""
    response = supabase.table('students').update({'voice_embedding': voice_embedding}).eq('student_id', student_id).execute()
    return response.data


# ========== END NEW FUNCTIONS ==========


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
        
        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)
    
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