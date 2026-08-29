# Tech With Eunice Learning Platform - Setup Guide

## 🚀 Quick Start (Deploy in 10 minutes)

### Step 1: Create a GitHub Repository
1. Go to **github.com**
2. Click **"New repository"**
3. Name it: `tech-with-eunice-platform`
4. Click **"Create repository"**

### Step 2: Upload Files to GitHub
1. Click **"Add file"** → **"Upload files"**
2. Upload these 3 files:
   - `app.py` (the main platform)
   - `requirements.txt` (dependencies)
   - `README.md` (this file)
3. Click **"Commit changes"**

### Step 3: Deploy to Streamlit Cloud
1. Go to **streamlit.io**
2. Click **"Sign up"** → Use GitHub to sign in
3. Click **"Create app"**
4. Select your repository: `tech-with-eunice-platform`
5. Select branch: `main`
6. Set file path to: `app.py`
7. Click **"Deploy"**
8. **Done!** Your platform is live! 🎉

---

## 📝 Login Credentials

### Admin (Instructor) Login
- **Password:** `admin123` (⚠️ Change this immediately!)
- Access: Full control of platform

### Student Login
- **Email:** Each student's email (used as password)
- **Password:** Their email address
- Access: View materials, submit assignments, track progress

---

## 🎯 Features Included

### ✅ Admin Dashboard
- **📊 Students:** Add/manage students with profiles
- **📅 Content Calendar:** Create weekly announcements, assignments, links
- **📝 Quizzes:** Build and manage quizzes
- **✅ Submissions:** Review student submissions
- **⚙️ Settings:** Configure cohort info

### ✅ Student Dashboard
- **📚 Course Materials:** Access weekly content by topic
- **📝 Assignments:** Download and submit assignments
- **🏆 Progress:** Track learning progress
- **📜 Certificate:** View certification status

---

## 🔐 Security

⚠️ **IMPORTANT:** After deployment, change the admin password!

To change admin password:
1. Open `app.py`
2. Find line: `return hash_password(password) == hash_password("admin123")`
3. Replace `"admin123"` with your secure password
4. Commit and push to GitHub
5. Streamlit automatically redeploys

---

## 📊 How Students Use It

1. **Go to your platform URL** (e.g., https://tech-with-eunice-platform.streamlit.app)
2. **Click "Student"**
3. **Select their name** from the dropdown
4. **Password:** Enter their email
5. **Dashboard:**
   - View weekly materials
   - Download assignments
   - Submit completed work
   - Check progress

---

## 👨‍🏫 How You (Admin) Use It

1. **Login as Instructor**
2. **Password:** `admin123` (or your custom password)
3. **Add Students:**
   - Go to "Students" tab
   - Click "Add New Student"
   - Enter: Name, Email, Gender

4. **Create Weekly Content:**
   - Go to "Content Calendar" tab
   - Add announcements, assignments, links
   - Set due dates
   - Students see it immediately

5. **Create Quizzes:**
   - Go to "Quizzes" tab
   - Build quiz with questions
   - Students can take it in their dashboard

6. **Review Submissions:**
   - Go to "Submissions" tab
   - See all student work submitted
   - Track who's completed what

---

## 💾 Data Storage

All data is stored in JSON files automatically:
- `students.json` - Student profiles
- `content.json` - Course materials
- `submissions.json` - Student submissions
- `quizzes.json` - Quiz questions

These files sync automatically to Streamlit Cloud.

---

## 🔗 Live Class Integration

For Google Meet classes:
1. **In Content Calendar**, add a link to your Google Meet
2. Students see the link and can join directly
3. Share the meeting link in announcements

---

## 📧 Email Reminders (Coming Soon)

Currently, you send reminders manually. To automate:
- I can add email notifications later
- Requires SMTP setup (optional)

---

## 🆘 Troubleshooting

**Q: Students can't login?**
A: Make sure their email in the system matches their password exactly

**Q: Content not showing?**
A: Refresh the page (Ctrl+Shift+R) or hard reload

**Q: Want to add more features?**
A: Reach out and I can expand the platform

---

## 📞 Support

For questions or issues:
- Email: techwitheunice@gmail.com
- Contact: Your developer

---

## 🎓 Cohort Timeline

- **Weeks 1-4:** Excel Fundamentals
- **Weeks 5-8:** SQL Database Foundations  
- **Weeks 9-11:** Power BI Dashboarding
- **Week 12:** GitHub for Portfolio
- **Week 13:** Capstone Presentations & Certification

Use the platform to deliver all course materials, assignments, and track student progress throughout!

---

**Happy teaching! Good luck with your cohort! 🚀**
