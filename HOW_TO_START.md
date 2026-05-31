# 🚀 How to Start SkillSync

## Quick Start (Recommended)

### Option 1: Click the Startup Script (Easiest)
1. Double-click **`START_APP.bat`** in the project folder
2. The app will start automatically and open in your browser

### Option 2: PowerShell Script
1. Right-click on **`START_APP.ps1`** 
2. Select "Run with PowerShell"
3. The app will start and open in your browser

### Option 3: Manual Terminal Start
```
cd "c:\Users\HP\Documents\Skill gap analyser"
.\.venv\Scripts\python.exe -m streamlit run app/main.py
```

---

## 🔧 Troubleshooting

### Error: "Connection Refused" on localhost:8501

**Solution 1: Check if port 8501 is available**
```
netstat -ano | findstr :8501
```
If something is using it, close that application or use a different port:
```
.\.venv\Scripts\python.exe -m streamlit run app/main.py --server.port=8502
```

**Solution 2: Clear cache and restart**
```
cd "c:\Users\HP\Documents\Skill gap analyser"
rm -Force -Recurse .streamlit 2>$null
rm -Force -Recurse __pycache__ 2>$null
rm -Force -Recurse app/__pycache__ 2>$null
.\.venv\Scripts\python.exe -m streamlit run app/main.py
```

**Solution 3: Restart your laptop** (clears all port locks)
Then use START_APP.bat

---

## 📝 First Time Usage

1. **Upload Resume** (📄 Resume Analysis)
   - Upload your resume file (PDF, DOCX, or TXT)
   - System will extract your skills automatically

2. **Add Job Description** (💼 Job Matching)
   - Paste or type a job description
   - Click "Calculate ATS Score" to see the match

3. **Check Skill Gaps** (🎯 Skill Gap)
   - System shows skills you have ✅
   - Shows skills you need to learn ❌
   - Match percentage calculated

4. **Get Recommendations** (📚 Recommendations)
   - See learning resources for missing skills

5. **Career Prediction** (🔮 Career Prediction)
   - Explore career paths based on your skills

---

## 🆘 Still Having Issues?

**Check if Python is working:**
```
python --version
```

**Check if Streamlit is installed:**
```
.\.venv\Scripts\python.exe -m streamlit --version
```

**Reinstall dependencies:**
```
.\.venv\Scripts\pip.exe install -r requirements.txt
```

---

## 📱 Default URL
**http://localhost:8501**

If you changed the port, it will be:
- **http://localhost:8502** (if using port 8502)
- **http://localhost:PORT_NUMBER** (for any other port)

---

## ⚠️ Important Notes

✅ Keep the terminal window open while using the app  
✅ First startup may take 5-10 seconds  
✅ Browser should open automatically  
✅ Use Ctrl+C in terminal to stop the app  

---

**Enjoy SkillSync!** 🎉
