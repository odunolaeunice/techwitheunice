import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import hashlib
import io

# Page config
st.set_page_config(page_title="Tech With Eunice LMS", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; }
    .success { color: #28a745; }
    .warning { color: #ff6b35; }
    .badge { display: inline-block; background: #ff6b35; color: white; padding: 5px 10px; border-radius: 5px; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# Data files
STUDENTS_FILE = "students.json"
CONTENT_FILE = "content.json"
ASSIGNMENTS_FILE = "assignments.json"
SUBMISSIONS_FILE = "submissions.json"
QUIZZES_FILE = "quizzes.json"
GRADES_FILE = "grades.json"
ANNOUNCEMENTS_FILE = "announcements.json"
ATTENDANCE_FILE = "attendance.json"
FEEDBACK_FILE = "feedback.json"

def init_data_files():
    for f in [STUDENTS_FILE, CONTENT_FILE, ASSIGNMENTS_FILE, SUBMISSIONS_FILE, 
              QUIZZES_FILE, GRADES_FILE, ANNOUNCEMENTS_FILE, ATTENDANCE_FILE, FEEDBACK_FILE]:
        if not os.path.exists(f):
            with open(f, 'w') as file:
                json.dump([], file)

init_data_files()

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_admin_password(password):
    return hash_password(password) == hash_password("admin123")

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'current_student_id' not in st.session_state:
    st.session_state.current_student_id = None

# ADMIN DASHBOARD
def admin_dashboard():
    st.markdown("<div class='header'><h1>🎓 Tech With Eunice - Admin Dashboard</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["📊 Students", "📅 Content", "📝 Quizzes", "📋 Assignments", "📈 Grades", "📢 Announcements", "✅ Attendance", "⚙️ Settings"])
    
    # TAB 1: Students
    with tab1:
        st.subheader("Student Management")
        students = load_json(STUDENTS_FILE)
        st.write(f"**Total Students:** {len(students)}")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("➕ Add Student"):
                st.session_state.show_add_student = True
        
        if st.session_state.get('show_add_student'):
            with st.form("add_student"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                if st.form_submit_button("Add"):
                    new_student = {
                        "id": len(students) + 1,
                        "name": name,
                        "email": email,
                        "gender": gender,
                        "joined": datetime.now().strftime("%Y-%m-%d"),
                        "progress": 0,
                        "current_week": 1
                    }
                    students.append(new_student)
                    save_json(STUDENTS_FILE, students)
                    st.success(f"✅ {name} added!")
                    st.session_state.show_add_student = False
                    st.rerun()
        
        if students:
            df = pd.DataFrame(students)
            st.dataframe(df[['id', 'name', 'email', 'gender', 'current_week', 'progress']], use_container_width=True)
    
    # TAB 2: Content Calendar
    with tab2:
        st.subheader("Course Content Management")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("📤 Bulk Upload"):
                st.session_state.show_bulk_upload = True
        
        if st.session_state.get('show_bulk_upload'):
            st.write("**Upload CSV/Excel with columns:** Week, Type (Announcement/Assignment/Quiz/Link), Title, Description, DueDate, Link")
            uploaded_file = st.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx'])
            if uploaded_file:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                content = load_json(CONTENT_FILE)
                for _, row in df.iterrows():
                    new_content = {
                        "id": len(content) + 1,
                        "week": int(row['Week']),
                        "type": row['Type'],
                        "title": row['Title'],
                        "description": row['Description'],
                        "due_date": str(row['DueDate']) if 'DueDate' in row.columns else "",
                        "link": str(row['Link']) if 'Link' in row.columns else "",
                        "created": datetime.now().strftime("%Y-%m-%d")
                    }
                    content.append(new_content)
                save_json(CONTENT_FILE, content)
                st.success(f"✅ {len(df)} items uploaded!")
                st.session_state.show_bulk_upload = False
                st.rerun()
        
        with st.form("add_content"):
            col1, col2 = st.columns(2)
            with col1:
                week = st.selectbox("Week", list(range(1, 14)))
                content_type = st.selectbox("Type", ["Course Material", "Announcement", "Assignment", "Quiz", "Link"])
            with col2:
                title = st.text_input("Title")
                description = st.text_area("Description")
            
            col1, col2 = st.columns(2)
            with col1:
                due_date = st.date_input("Due Date (optional)")
            with col2:
                link = st.text_input("Link (optional)")
            
            # File upload for course materials
            if content_type == "Course Material":
                uploaded_file = st.file_uploader("Upload PDF or PPTX", type=['pdf', 'pptx'], key="material_upload")
            else:
                uploaded_file = None
            
            if st.form_submit_button("Add Content"):
                content = load_json(CONTENT_FILE)
                
                file_name = ""
                file_type = ""
                if uploaded_file and content_type == "Course Material":
                    file_name = uploaded_file.name
                    file_type = uploaded_file.type
                
                new_item = {
                    "id": len(content) + 1,
                    "week": week,
                    "type": content_type,
                    "title": title,
                    "description": description,
                    "due_date": str(due_date),
                    "link": link,
                    "file_name": file_name,
                    "file_type": file_type,
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
                content.append(new_item)
                save_json(CONTENT_FILE, content)
                st.success("✅ Content added!")
                st.rerun()
        
        content = load_json(CONTENT_FILE)
        if content:
            st.write("**Manage Content:**")
            for item in content:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**Week {item['week']}:** {item['type']} - {item['title']}")
                with col2:
                    st.caption(f"Due: {item['due_date']}")
                with col3:
                    if st.button("🗑️", key=f"del_content_{item['id']}"):
                        content = [c for c in content if c['id'] != item['id']]
                        save_json(CONTENT_FILE, content)
                        st.success("✅ Deleted!")
                        st.rerun()
    
    # TAB 3: Quizzes
    with tab3:
        st.subheader("Quiz Management")
        quizzes = load_json(QUIZZES_FILE)
        
        with st.form("create_quiz"):
            week = st.selectbox("Week", list(range(1, 14)), key="quiz_week")
            quiz_title = st.text_input("Quiz Title")
            num_questions = st.number_input("Questions", min_value=1, max_value=10, value=3)
            
            questions = []
            for i in range(num_questions):
                st.write(f"**Q{i+1}**")
                q_text = st.text_input(f"Question", key=f"q_{i}")
                q_options = st.text_area(f"Options (comma-separated)", key=f"opt_{i}")
                q_correct = st.text_input(f"Correct answer", key=f"correct_{i}")
                questions.append({
                    "question": q_text,
                    "options": [o.strip() for o in q_options.split(",")],
                    "correct": q_correct
                })
            
            if st.form_submit_button("Create Quiz"):
                new_quiz = {
                    "id": len(quizzes) + 1,
                    "week": week,
                    "title": quiz_title,
                    "questions": questions,
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
                quizzes.append(new_quiz)
                save_json(QUIZZES_FILE, quizzes)
                st.success("✅ Quiz created!")
                st.rerun()
        
        if quizzes:
            st.write(f"**Total Quizzes:** {len(quizzes)}")
            for quiz in quizzes:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"Week {quiz['week']}: {quiz['title']} ({len(quiz['questions'])} questions)")
                with col2:
                    if st.button("🗑️", key=f"del_quiz_{quiz['id']}"):
                        quizzes = [q for q in quizzes if q['id'] != quiz['id']]
                        save_json(QUIZZES_FILE, quizzes)
                        st.success("✅ Quiz deleted!")
                        st.rerun()
    
    # TAB 4: Assignments & Submissions
    with tab4:
        st.subheader("Assignment Management")
        assignments = load_json(ASSIGNMENTS_FILE)
        
        with st.form("add_assignment"):
            week = st.selectbox("Week", list(range(1, 14)), key="assign_week")
            title = st.text_input("Assignment Title")
            description = st.text_area("Description")
            due_date = st.date_input("Due Date")
            
            if st.form_submit_button("Create Assignment"):
                new_assign = {
                    "id": len(assignments) + 1,
                    "week": week,
                    "title": title,
                    "description": description,
                    "due_date": str(due_date),
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
                assignments.append(new_assign)
                save_json(ASSIGNMENTS_FILE, assignments)
                st.success("✅ Assignment created!")
                st.rerun()
        
        if assignments:
            st.write(f"**Total Assignments:** {len(assignments)}")
            for assign in assignments:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"Week {assign['week']}: {assign['title']} (Due: {assign['due_date']})")
                with col2:
                    if st.button("🗑️", key=f"del_assign_{assign['id']}"):
                        assignments = [a for a in assignments if a['id'] != assign['id']]
                        save_json(ASSIGNMENTS_FILE, assignments)
                        st.success("✅ Assignment deleted!")
                        st.rerun()
        
        st.write("---")
        st.subheader("Student Submissions")
        submissions = load_json(SUBMISSIONS_FILE)
        if submissions:
            for sub in submissions:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                    with col1:
                        st.write(f"**{sub['student_name']}**")
                    with col2:
                        st.write(f"**{sub['assignment']}**")
                    with col3:
                        if sub.get('google_drive_link'):
                            st.markdown(f"[📄 Open File]({sub['google_drive_link']})")
                    with col4:
                        st.caption(sub['submitted'])
                    if sub.get('notes'):
                        st.caption(f"Notes: {sub['notes']}")
                    st.divider()
        else:
            st.info("No submissions yet")
    
    # TAB 5: Grades & Quiz Results
    with tab5:
        grade_tab1, grade_tab2 = st.tabs(["📋 Assignment Grades", "📊 Quiz Results"])
        
        with grade_tab1:
            st.subheader("Grade Assignment Submissions")
            students = load_json(STUDENTS_FILE)
            submissions = load_json(SUBMISSIONS_FILE)
            
            if students and submissions:
                selected_student = st.selectbox("Select Student", [s['name'] for s in students])
                student = next((s for s in students if s['name'] == selected_student), None)
                
                student_subs = [s for s in submissions if s['student_id'] == student['id']]
                
                if student_subs:
                    for sub in student_subs:
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**{sub['assignment']}**")
                        with col2:
                            grade = st.number_input(f"Grade", min_value=0, max_value=100, value=0, key=f"grade_{sub['id']}")
                        with col3:
                            if st.button("Save", key=f"save_{sub['id']}"):
                                grades = load_json(GRADES_FILE)
                                existing = next((g for g in grades if g['student_id'] == student['id'] and g['assignment_id'] == sub['id']), None)
                                if existing:
                                    existing['grade'] = grade
                                else:
                                    grades.append({
                                        "student_id": student['id'],
                                        "assignment_id": sub['id'],
                                        "assignment": sub['assignment'],
                                        "grade": grade
                                    })
                                save_json(GRADES_FILE, grades)
                                st.success("✅ Grade saved!")
            else:
                st.info("No submissions yet")
        
        with grade_tab2:
            st.subheader("Student Quiz Results")
            if os.path.exists("quiz_results.json"):
                quiz_results = load_json("quiz_results.json")
                if quiz_results:
                    students = load_json(STUDENTS_FILE)
                    selected_student = st.selectbox("Select Student", [s['name'] for s in students], key="quiz_student")
                    student = next((s for s in students if s['name'] == selected_student), None)
                    
                    student_quizzes = [q for q in quiz_results if q['student_id'] == student['id']]
                    
                    if student_quizzes:
                        for quiz in student_quizzes:
                            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                            with col1:
                                st.write(f"**Week {quiz['week']}: {quiz['quiz_title']}**")
                            with col2:
                                st.write(f"Score: {quiz['score']}/{quiz['total']}")
                            with col3:
                                percentage_color = "🟢" if quiz['percentage'] >= 70 else "🔴"
                                st.write(f"{percentage_color} {quiz['percentage']:.0f}%")
                            with col4:
                                st.caption(quiz['submitted'])
                    else:
                        st.info("No quiz attempts yet")
                else:
                    st.info("No quiz results yet")
            else:
                st.info("No quiz results yet")
    
    # TAB 6: Announcements
    with tab6:
        st.subheader("Broadcast to All Students")
        
        with st.form("announce"):
            title = st.text_input("Announcement Title")
            message = st.text_area("Message")
            
            if st.form_submit_button("Send Announcement"):
                announcements = load_json(ANNOUNCEMENTS_FILE)
                new_announce = {
                    "id": len(announcements) + 1,
                    "title": title,
                    "message": message,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "read_by": []
                }
                announcements.append(new_announce)
                save_json(ANNOUNCEMENTS_FILE, announcements)
                st.success("✅ Announcement sent to all students!")
        
        st.write("---")
        st.subheader("Manage Announcements")
        announcements = load_json(ANNOUNCEMENTS_FILE)
        if announcements:
            for announce in reversed(announcements):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{announce['title']}** - {announce['date']}")
                with col2:
                    if st.button("🗑️", key=f"del_announce_{announce['id']}"):
                        announcements = [a for a in announcements if a['id'] != announce['id']]
                        save_json(ANNOUNCEMENTS_FILE, announcements)
                        st.success("✅ Announcement deleted!")
                        st.rerun()
    
    # TAB 7: Attendance
    with tab7:
        st.subheader("Class Attendance")
        attendance = load_json(ATTENDANCE_FILE)
        students = load_json(STUDENTS_FILE)
        
        if attendance and students:
            attendance_df = pd.DataFrame(attendance)
            st.dataframe(attendance_df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Records", len(attendance))
        else:
            st.info("No attendance records yet. They auto-track when students click live class links.")
    
    # TAB 8: Settings
    with tab8:
        st.subheader("Cohort Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Cohort Information**")
            st.write("- Duration: 13 weeks (Sep-Nov 2026)")
            st.write("- Classes: Twice weekly")
            st.write("- Cost: ₦50,000")
        
        with col2:
            st.write("**Curriculum**")
            st.write("- Weeks 1-4: Excel")
            st.write("- Weeks 5-8: SQL")
            st.write("- Weeks 9-11: Power BI")
            st.write("- Week 12: GitHub")
            st.write("- Week 13: Presentations")

# STUDENT DASHBOARD
def student_dashboard(student_id):
    students = load_json(STUDENTS_FILE)
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        st.error("Student not found")
        return
    
    st.markdown(f"<div class='header'><h1>Welcome, {student['name']}! 👋</h1></div>", unsafe_allow_html=True)
    
    # Check weekly unlock
    current_week = student['current_week']
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📚 Materials", "📝 Quizzes", "📋 Assignments", "📊 Progress", "📢 Announcements", "📝 Feedback"])
    
    # TAB 1: Course Materials
    with tab1:
        st.subheader(f"Week {current_week} - Course Materials")
        content = load_json(CONTENT_FILE)
        week_content = [c for c in content if c['week'] == current_week]
        
        if week_content:
            for item in week_content:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{item['type']}:** {item['title']}")
                        st.write(item['description'])
                        
                        # Show file if it's a course material
                        if item['type'] == "Course Material" and item.get('file_name'):
                            st.info(f"📄 **File:** {item['file_name']}")
                            st.caption(f"Type: {item.get('file_type', 'PDF/PPTX')}")
                        
                        # Show link if available
                        if item['link']:
                            st.markdown(f"🔗 [Access Material]({item['link']})")
                    with col2:
                        st.checkbox(f"Completed", key=f"material_{item['id']}")
                    st.divider()
        else:
            st.info("No materials for this week yet")
    
    # TAB 2: Quizzes
    with tab2:
        st.subheader(f"Week {current_week} - Quiz")
        quizzes = load_json(QUIZZES_FILE)
        week_quiz = next((q for q in quizzes if q['week'] == current_week), None)
        
        if week_quiz:
            score = 0
            answers = []
            for i, q in enumerate(week_quiz['questions']):
                st.write(f"**Q{i+1}: {q['question']}**")
                answer = st.radio("Select answer", q['options'], key=f"q_{i}")
                answers.append(answer)
                if answer == q['correct']:
                    score += 1
            
            if st.button("Submit Quiz"):
                percentage = (score / len(week_quiz['questions'])) * 100
                st.success(f"✅ Score: {score}/{len(week_quiz['questions'])} ({percentage:.0f}%)")
                
                # Save quiz result
                quiz_results = load_json("quiz_results.json") if os.path.exists("quiz_results.json") else []
                quiz_result = {
                    "id": len(quiz_results) + 1,
                    "student_id": student_id,
                    "student_name": student['name'],
                    "week": current_week,
                    "quiz_title": week_quiz['title'],
                    "score": score,
                    "total": len(week_quiz['questions']),
                    "percentage": percentage,
                    "submitted": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                quiz_results.append(quiz_result)
                save_json("quiz_results.json", quiz_results)
                
                # Update progress if score >= 70%
                if percentage >= 70:
                    students = load_json(STUDENTS_FILE)
                    # Add ~7.7% per week (100% / 13 weeks)
                    student['progress'] = min(100, student['progress'] + int(100/13))
                    if student['current_week'] < 13:
                        student['current_week'] += 1
                    idx = next((i for i, s in enumerate(students) if s['id'] == student_id), None)
                    students[idx] = student
                    save_json(STUDENTS_FILE, students)
                    st.info("🎉 Score 70%+ - Week unlocked!")
                    st.rerun()
                else:
                    st.warning(f"⚠️ Score below 70%. Try again to unlock next week!")
        else:
            st.info("No quiz this week")
    
    # TAB 3: Assignments
    with tab3:
        st.subheader(f"Week {current_week} - Assignment Submission")
        assignments = load_json(ASSIGNMENTS_FILE)
        week_assign = [a for a in assignments if a['week'] == current_week]
        submissions = load_json(SUBMISSIONS_FILE)
        
        if week_assign:
            for assign in week_assign:
                st.write(f"**{assign['title']}**")
                st.write(assign['description'])
                st.caption(f"Due: {assign['due_date']}")
                
                # Show previous submissions
                my_submissions = [s for s in submissions if s['student_id'] == student_id and s['assignment_id'] == assign['id']]
                if my_submissions:
                    st.info("**Your Submissions:**")
                    for sub in my_submissions:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"📤 Submitted: {sub['submitted']}")
                            if sub.get('google_drive_link'):
                                st.markdown(f"🔗 [View File]({sub['google_drive_link']})")
                        with col2:
                            st.caption("Status: Submitted")
                        with col3:
                            if st.button("🗑️ Delete", key=f"del_sub_{sub['id']}"):
                                submissions = [s for s in submissions if s['id'] != sub['id']]
                                save_json(SUBMISSIONS_FILE, submissions)
                                st.success("✅ Submission deleted!")
                                st.rerun()
                
                # New submission form
                with st.form(f"submit_{assign['id']}"):
                    google_drive_link = st.text_input("Google Drive Link (paste your shared file link)", key=f"link_{assign['id']}")
                    notes = st.text_area("Notes (optional)", key=f"notes_{assign['id']}")
                    
                    if st.form_submit_button("Submit Assignment"):
                        if google_drive_link:
                            submissions = load_json(SUBMISSIONS_FILE)
                            new_sub = {
                                "id": len(submissions) + 1,
                                "student_id": student_id,
                                "student_name": student['name'],
                                "assignment": assign['title'],
                                "assignment_id": assign['id'],
                                "google_drive_link": google_drive_link,
                                "notes": notes,
                                "submitted": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "status": "Submitted"
                            }
                            submissions.append(new_sub)
                            save_json(SUBMISSIONS_FILE, submissions)
                            st.success("✅ Assignment submitted!")
                            st.rerun()
                        else:
                            st.error("❌ Please paste your Google Drive link")
                
                st.divider()
        else:
            st.info("No assignment this week")
    
    # TAB 4: Progress
    with tab4:
        st.subheader("Your Learning Progress")
        st.progress(student['progress'] / 100)
        st.metric("Progress", f"{student['progress']}%")
        st.metric("Current Week", current_week)
        
        if student['progress'] == 100:
            st.success("🎓 You've completed the cohort!")
    
    # TAB 5: Announcements
    with tab5:
        st.subheader("Announcements")
        announcements = load_json(ANNOUNCEMENTS_FILE)
        
        if announcements:
            for announce in reversed(announcements):
                with st.container():
                    st.write(f"**{announce['title']}**")
                    st.write(announce['message'])
                    st.caption(announce['date'])
                    st.divider()
        else:
            st.info("No announcements yet")
    
    # TAB 6: Feedback
    with tab6:
        st.subheader("Instructor Feedback")
        feedback = load_json(FEEDBACK_FILE)
        student_feedback = [f for f in feedback if f['student_id'] == student_id]
        
        if student_feedback:
            for fb in student_feedback:
                with st.container():
                    st.write(f"**{fb['assignment']}**")
                    st.write(fb['feedback'])
                    st.caption(f"Grade: {fb.get('grade', 'N/A')}")
                    st.divider()
        else:
            st.info("No feedback yet")

# MAIN APP
def main():
    st.sidebar.title("Tech With Eunice LMS")
    
    if not st.session_state.logged_in:
        st.markdown("<div class='header'><h1>🎓 Tech With Eunice Learning Platform</h1></div>", unsafe_allow_html=True)
        
        login_type = st.radio("Login as:", ["Student", "Instructor"])
        
        if login_type == "Student":
            st.subheader("Student Login")
            students = load_json(STUDENTS_FILE)
            student_names = {s['name']: s['id'] for s in students}
            
            if student_names:
                selected = st.selectbox("Select your name", list(student_names.keys()))
                password = st.text_input("Password (your email)", type="password")
                
                if st.button("Login"):
                    student = next((s for s in students if s['name'] == selected), None)
                    if student and password == student['email']:
                        st.session_state.logged_in = True
                        st.session_state.user_type = "student"
                        st.session_state.current_student_id = student['id']
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            else:
                st.warning("No students registered yet")
        
        else:
            st.subheader("Instructor Login")
            admin_pass = st.text_input("Admin Password", type="password")
            
            if st.button("Login as Instructor"):
                if check_admin_password(admin_pass):
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.rerun()
                else:
                    st.error("Invalid password")
    
    else:
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
