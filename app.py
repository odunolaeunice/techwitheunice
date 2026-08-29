import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib

# Page config
st.set_page_config(page_title="Tech With Eunice Learning Platform", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; }
    .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 10px 0; }
    .success { color: #28a745; font-weight: bold; }
    .warning { color: #ff6b35; font-weight: bold; }
    .danger { color: #dc3545; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Data files
STUDENTS_FILE = "students.json"
CONTENT_FILE = "content.json"
SUBMISSIONS_FILE = "submissions.json"
QUIZZES_FILE = "quizzes.json"

# Initialize data files
def init_data_files():
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(CONTENT_FILE):
        with open(CONTENT_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(QUIZZES_FILE):
        with open(QUIZZES_FILE, 'w') as f:
            json.dump([], f)

init_data_files()

# Load data
def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Authentication
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_admin_password(password):
    # Default admin password: admin123 (change this!)
    return hash_password(password) == hash_password("admin123")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'current_student_id' not in st.session_state:
    st.session_state.current_student_id = None

# ADMIN DASHBOARD
def admin_dashboard():
    st.markdown("<div class='header'><h1>🎓 Tech With Eunice - Admin Dashboard</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Students", "📅 Content Calendar", "📝 Quizzes", "✅ Submissions", "⚙️ Settings"])
    
    # TAB 1: Students
    with tab1:
        st.subheader("Student Management")
        students = load_json(STUDENTS_FILE)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**Total Students:** {len(students)}")
        with col2:
            if st.button("➕ Add New Student"):
                st.session_state.show_add_student = True
        
        if st.session_state.get('show_add_student'):
            with st.form("add_student_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                picture = st.file_uploader("Profile Picture")
                submitted = st.form_submit_button("Add Student")
                
                if submitted:
                    new_student = {
                        "id": len(students) + 1,
                        "name": name,
                        "email": email,
                        "gender": gender,
                        "joined_date": datetime.now().strftime("%Y-%m-%d"),
                        "progress": 0
                    }
                    students.append(new_student)
                    save_json(STUDENTS_FILE, students)
                    st.success(f"✅ {name} added!")
                    st.session_state.show_add_student = False
                    st.rerun()
        
        # Display students
        if students:
            df = pd.DataFrame(students)
            st.dataframe(df, use_container_width=True)
    
    # TAB 2: Content Calendar
    with tab2:
        st.subheader("Weekly Content Calendar")
        content = load_json(CONTENT_FILE)
        
        with st.form("add_content_form"):
            week = st.selectbox("Week", list(range(1, 14)))
            content_type = st.selectbox("Content Type", ["Announcement", "Assignment", "Quiz", "Link"])
            title = st.text_input("Title")
            description = st.text_area("Description/Details")
            due_date = st.date_input("Due Date (if applicable)")
            
            if content_type == "Link":
                link = st.text_input("Link URL")
            else:
                link = ""
            
            submitted = st.form_submit_button("Add Content")
            
            if submitted:
                new_content = {
                    "id": len(content) + 1,
                    "week": week,
                    "type": content_type,
                    "title": title,
                    "description": description,
                    "due_date": str(due_date),
                    "link": link,
                    "created_date": datetime.now().strftime("%Y-%m-%d")
                }
                content.append(new_content)
                save_json(CONTENT_FILE, content)
                st.success("✅ Content added!")
                st.rerun()
        
        # Display content calendar
        if content:
            df = pd.DataFrame(content)
            st.dataframe(df, use_container_width=True)
    
    # TAB 3: Quizzes
    with tab3:
        st.subheader("Quiz Management")
        quizzes = load_json(QUIZZES_FILE)
        
        with st.form("add_quiz_form"):
            week = st.selectbox("Week", list(range(1, 14)), key="quiz_week")
            quiz_title = st.text_input("Quiz Title")
            num_questions = st.number_input("Number of Questions", min_value=1, max_value=10)
            
            questions = []
            for i in range(num_questions):
                st.write(f"**Question {i+1}**")
                q_text = st.text_input(f"Question {i+1}", key=f"q_{i}")
                q_options = st.text_area(f"Options (comma-separated)", key=f"opt_{i}")
                q_correct = st.text_input(f"Correct Answer", key=f"correct_{i}")
                questions.append({
                    "question": q_text,
                    "options": q_options.split(","),
                    "correct": q_correct
                })
            
            submitted = st.form_submit_button("Create Quiz")
            
            if submitted:
                new_quiz = {
                    "id": len(quizzes) + 1,
                    "week": week,
                    "title": quiz_title,
                    "questions": questions,
                    "created_date": datetime.now().strftime("%Y-%m-%d")
                }
                quizzes.append(new_quiz)
                save_json(QUIZZES_FILE, quizzes)
                st.success("✅ Quiz created!")
                st.rerun()
    
    # TAB 4: Submissions
    with tab4:
        st.subheader("Student Submissions")
        submissions = load_json(SUBMISSIONS_FILE)
        if submissions:
            df = pd.DataFrame(submissions)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No submissions yet")
    
    # TAB 5: Settings
    with tab5:
        st.subheader("Platform Settings")
        st.write("**Cohort Info**")
        st.write("- Duration: 13 weeks (September–November 2026)")
        st.write("- Classes: Twice weekly (Google Meet)")
        st.write("- Cost: ₦50,000 (Full payment before class starts)")
        
        st.write("\n**Curriculum Breakdown**")
        st.write("""
        - Weeks 1-4: Excel Fundamentals
        - Weeks 5-8: SQL Database Foundations
        - Weeks 9-11: Power BI Dashboarding
        - Week 12: GitHub for Hosting & Portfolio
        - Week 13: Capstone Presentations & Certification
        """)

# STUDENT DASHBOARD
def student_dashboard(student_id):
    students = load_json(STUDENTS_FILE)
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        st.error("Student not found")
        return
    
    st.markdown(f"<div class='header'><h1>Welcome, {student['name']}! 👋</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Course Materials", "📝 Assignments", "🏆 Progress", "📜 Certificate"])
    
    # TAB 1: Course Materials
    with tab1:
        st.subheader("Weekly Content")
        content = load_json(CONTENT_FILE)
        
        # Filter by week
        weeks = sorted(set([c['week'] for c in content]))
        selected_week = st.selectbox("Select Week", weeks if weeks else [1])
        
        week_content = [c for c in content if c['week'] == selected_week]
        
        if week_content:
            for item in week_content:
                with st.container():
                    st.write(f"**{item['type']}:** {item['title']}")
                    st.write(item['description'])
                    if item['link']:
                        st.markdown(f"[🔗 Open Link]({item['link']})")
                    if item['due_date']:
                        st.caption(f"Due: {item['due_date']}")
                    st.divider()
        else:
            st.info("No content for this week yet")
    
    # TAB 2: Assignments
    with tab2:
        st.subheader("Submit Assignment")
        content = load_json(CONTENT_FILE)
        assignments = [c for c in content if c['type'] == "Assignment"]
        
        if assignments:
            selected_assignment = st.selectbox("Select Assignment", [a['title'] for a in assignments])
            assignment = next((a for a in assignments if a['title'] == selected_assignment), None)
            
            st.write(f"**Due:** {assignment['due_date']}")
            
            with st.form("submit_assignment"):
                submitted_file = st.file_uploader("Upload Assignment")
                notes = st.text_area("Notes (optional)")
                submitted = st.form_submit_button("Submit Assignment")
                
                if submitted and submitted_file:
                    submissions = load_json(SUBMISSIONS_FILE)
                    new_submission = {
                        "student_id": student_id,
                        "student_name": student['name'],
                        "assignment": selected_assignment,
                        "submitted_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "status": "Submitted"
                    }
                    submissions.append(new_submission)
                    save_json(SUBMISSIONS_FILE, submissions)
                    st.success("✅ Assignment submitted!")
    
    # TAB 3: Progress
    with tab3:
        st.subheader("Your Progress")
        st.progress(student['progress'] / 100)
        st.write(f"**Progress:** {student['progress']}%")
    
    # TAB 4: Certificate
    with tab4:
        st.subheader("Certificate of Completion")
        if student['progress'] == 100:
            st.success("🎓 You have completed the cohort!")
            st.write(f"Congratulations, {student['name']}!")
        else:
            st.info(f"Complete all modules to earn your certificate. Current progress: {student['progress']}%")

# MAIN APP
def main():
    st.sidebar.title("Tech With Eunice Learning Platform")
    
    if not st.session_state.logged_in:
        # Login Page
        st.markdown("<div class='header'><h1>🎓 Tech With Eunice Learning Platform</h1><p>September–November 2026 Cohort</p></div>", unsafe_allow_html=True)
        
        login_type = st.radio("I am a:", ["Student", "Instructor"])
        
        if login_type == "Student":
            st.subheader("Student Login")
            students = load_json(STUDENTS_FILE)
            student_names = {s['name']: s['id'] for s in students}
            
            if student_names:
                selected_student = st.selectbox("Select your name", list(student_names.keys()))
                password = st.text_input("Enter your password (use your email)", type="password")
                
                if st.button("Login"):
                    student = next((s for s in students if s['name'] == selected_student), None)
                    if student and password == student['email']:
                        st.session_state.logged_in = True
                        st.session_state.user_type = "student"
                        st.session_state.current_student_id = student['id']
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            else:
                st.warning("No students registered yet")
        
        else:  # Instructor
            st.subheader("Instructor Login")
            admin_password = st.text_input("Enter admin password", type="password")
            
            if st.button("Login as Instructor"):
                if check_admin_password(admin_password):
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.rerun()
                else:
                    st.error("Invalid admin password")
    
    else:
        # Logged in
        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.current_student_id = None
            st.rerun()
        
        if st.session_state.user_type == "admin":
            admin_dashboard()
        else:
            student_dashboard(st.session_state.current_student_id)

if __name__ == "__main__":
    main()
