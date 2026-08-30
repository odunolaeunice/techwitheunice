# Tech With Eunice Learning Platform
## Complete Setup Guide

---

## 🚀 DEPLOYMENT (10 minutes)

### Step 1: Create GitHub Repository
1. Go to **github.com**
2. Click **"New repository"**
3. Name: `tech-with-eunice-lms`
4. Click **"Create repository"**

### Step 2: Upload Files to GitHub
1. Click **"Add file"** → **"Upload files"**
2. Upload these 3 files:
   - `lms_app.py` (renamed to `app.py` on GitHub)
   - `lms_requirements.txt` (renamed to `requirements.txt`)
   - This file

3. Click **"Commit changes"**

### Step 3: Deploy to Streamlit Cloud
1. Go to **streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**
4. Select repository: `tech-with-eunice-lms`
5. Branch: `main`
6. Main file path: `app.py`
7. Click **"Deploy"** ✅

**Wait 2-3 minutes for deployment. Your LMS is LIVE!** 🎉

---

## 📝 LOGIN CREDENTIALS

### **INSTRUCTOR (You)**
- **Login as:** Instructor
- **Password:** `admin123`
- ⚠️ **CHANGE THIS IMMEDIATELY after first login!**

### **STUDENTS**
- **Login as:** Student
- **Name:** Their name (you add it)
- **Password:** Their email address

---

## 🎯 CORE FEATURES INCLUDED

### ✅ 1. Weekly Content Unlock System
- Content unlocks week-by-week as students progress
- Quiz + materials completion unlocks next week
- Prevents students from jumping ahead

### ✅ 2. Progress Tracker
- Week-by-week progress (0-100%)
- Auto-updates when students complete quizzes
- Shows current week

### ✅ 3. Auto-Graded Quizzes
- Create quizzes with multiple choice questions
- Students take quiz, auto-scored
- Perfect score = week completion
- Automatic week unlock

### ✅ 4. Assignment Management
- Create assignments per week
- Students upload files
- You manually grade (0-100)

### ✅ 5. Grade Tracker
- View all student grades
- Grade submissions one-by-one
- Track assignment performance

### ✅ 6. Live Class Links (Auto-Attendance)
- Post Google Meet links in content
- Students click → auto-tracked attendance
- Attendance data shows who joined

### ✅ 7. Class Recordings Access
- Post recording links in content
- Students access to watch/download
- Just paste the link in materials

### ✅ 8. Teacher Announcements (Broadcast)
- Send messages to ALL students at once
- Shows in student dashboard
- Date-stamped

### ✅ 9. Feedback/Comments
- Leave feedback on student assignments
- Grade attached to feedback
- Students see your comments

### ✅ 10. Bulk File Upload
- Upload CSV or Excel with all content at once
- Columns needed: Week, Type, Title, Description, DueDate, Link
- Saves 10 hours of manual entry

### ✅ 11. Settings Page
- View cohort configuration
- Curriculum timeline
- All stored settings

---

## 👨‍🏫 HOW TO USE (INSTRUCTOR)

### **First Time Setup:**

1. **Login** (Password: `admin123`)
2. **Add Students** (📊 Students tab)
   - Click "Add Student"
   - Enter: Name, Email, Gender
   - Repeat for all 5 students

3. **Upload Course Content** (📅 Content tab)
   - **Option A - Individual Entry:** Add content one-by-one
   - **Option B - Bulk Upload:** Upload CSV/Excel with all weeks at once

4. **Create Quizzes** (📝 Quizzes tab)
   - Week number
   - Quiz title
   - Questions with multiple choice options
   - Correct answers

5. **Create Assignments** (📋 Assignments tab)
   - Week number
   - Assignment title
   - Description
   - Due date

6. **Monitor Progress** (📊 various tabs)
   - See student submissions
   - Grade assignments (📈 Grades tab)
   - Leave feedback (Tab 9 in student view)

7. **Make Announcements** (📢 Announcements tab)
   - Send broadcast messages to all students
   - Shows up in their dashboard

---

## 👨‍🎓 HOW STUDENTS USE IT

### **Login:**
1. Go to your Streamlit URL
2. Click **"Student"**
3. Select their name
4. Password = Their email
5. Click **"Login"**

### **Student Dashboard:**
1. **📚 Materials** - Access weekly course materials
   - Checkbox to mark complete
   - Click links for Google Meet classes
   - Download recordings

2. **📝 Quizzes** - Take weekly quizzes
   - Auto-graded
   - Pass quiz → unlock next week

3. **📋 Assignments** - Submit homework
   - Upload files
   - See due dates

4. **📊 Progress** - Track learning journey
   - Percentage complete
   - Current week

5. **📢 Announcements** - Read teacher updates

6. **📝 Feedback** - View grades & comments

---

## 📊 CURRICULUM STRUCTURE

### **Weeks 1-4: Excel Fundamentals**
- Materials
- Quiz
- Assignment

### **Weeks 5-8: SQL Database Foundations**
- Materials
- Quiz
- Assignment

### **Weeks 9-11: Power BI Dashboarding**
- Materials
- Quiz
- Assignment

### **Week 12: GitHub & Portfolio**
- Materials
- Final assignment

### **Week 13: Capstone Presentations**
- Final projects
- Certification

---

## 📤 BULK UPLOAD FORMAT

Create a CSV or Excel file with these columns:

```
Week | Type | Title | Description | DueDate | Link
-----|------|-------|-------------|---------|-----
1 | Announcement | Welcome | Welcome to class | 2026-09-01 | 
1 | Link | Class Recording | Week 1 Recording | | https://yourdrive.com/video1
1 | Assignment | Exercise 1 | Complete Excel exercises | 2026-09-05 | 
2 | Quiz | Excel Quiz | 5 questions | 2026-09-08 | 
```

Upload this in Content tab → "Bulk Upload"
All items added automatically! ✅

---

## 🔒 SECURITY

### **Change Default Admin Password!**

1. Download `app.py` from your GitHub repo
2. Find line: `return hash_password(password) == hash_password("admin123")`
3. Replace `"admin123"` with your secure password
4. Upload updated file to GitHub
5. Streamlit auto-redeploys ✅

### **Protect Student Data:**
- Never share login credentials publicly
- Change password regularly
- Export grades before cohort ends

---

## 💾 DATA STORAGE

All data saved automatically in JSON files:
- `students.json` - Student profiles
- `content.json` - Course materials
- `quizzes.json` - Quiz questions
- `assignments.json` - Assignments
- `submissions.json` - Student work
- `grades.json` - Grades
- `announcements.json` - Messages
- `attendance.json` - Class attendance
- `feedback.json` - Instructor feedback

**Backup regularly!** Download these files weekly.

---

## 🆘 TROUBLESHOOTING

**Q: Students can't login?**
A: Check email spelling matches exactly. Password is their email address.

**Q: Progress not updating?**
A: Progress updates when quiz is perfectly scored. Update manually in Grades tab if needed.

**Q: Content not showing?**
A: Hard refresh (Ctrl+Shift+R). Check week number matches student's current week.

**Q: Want to add more features?**
A: Contact your developer. Platform is extensible.

---

## 📞 SUPPORT

For issues or questions:
- Email: techwitheunice@gmail.com
- Contact: Your developer

---

## ✅ LAUNCH CHECKLIST

- [ ] Repository created on GitHub
- [ ] Files uploaded: app.py, requirements.txt
- [ ] Deployed to Streamlit
- [ ] Login works (test as instructor & student)
- [ ] Added 5 students
- [ ] Uploaded course content (bulk or individual)
- [ ] Created quizzes
- [ ] Created assignments
- [ ] Tested student login
- [ ] Changed admin password
- [ ] Shared platform link with students

---

## 🎓 COHORT TIMELINE

**September 1, 2026:** Platform launches
**Weeks 1-4:** Excel training
**Weeks 5-8:** SQL training
**Weeks 9-11:** Power BI training
**Week 12:** Portfolio & GitHub setup
**Week 13:** Capstone presentations & certification

---

**You're all set! Deploy and start teaching! 🚀**

Questions? Need help? I'm here.

Good luck with your cohort! 🎉
