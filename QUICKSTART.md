# ⚡ QUICKSTART - 5-Minute Setup

Get SkillSync running in **5 minutes** with this quick guide.

## 🎯 One-Minute Summary

SkillSync analyzes your resume, matches it against job descriptions, identifies skill gaps, recommends learning resources, and predicts your career path.

## 📋 Prerequisites

- ✅ Python 3.8+ installed
- ✅ pip available
- ✅ 5 minutes of free time

## 🚀 Installation (2 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**What's being installed:**
- `streamlit` - Web app framework
- `pandas` - Data processing
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning
- `python-docx` - DOCX file reading
- `PyPDF2` - PDF file reading

### Step 2: Run the App

```bash
streamlit run app/main.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.x.x.x:8501
```

The app will automatically open in your browser! 🎉

## 📖 Using SkillSync (3 minutes)

### Quick Workflow:

1. **Upload Your Resume** (30 seconds)
   - Go to "📄 Resume Analysis" tab
   - Click "Upload your resume"
   - Select a PDF, DOCX, or TXT file
   - View extracted information

2. **Paste Job Description** (30 seconds)
   - Go to "💼 Job Matching" tab
   - Paste a job description
   - Click "Calculate ATS Score"
   - See how well you match

3. **View Skill Gap** (30 seconds)
   - Go to "🎯 Skill Gap" tab
   - See matched, missing, and excess skills
   - Check learning timeline

4. **Get Recommendations** (30 seconds)
   - Go to "📚 Recommendations" tab
   - Browse recommended courses
   - Add to your learning plan

5. **Career Prediction** (30 seconds)
   - Go to "🔮 Career Prediction" tab
   - View predicted career paths
   - See development recommendations

## 🔥 Advanced Features

### Database Setup (Optional)

Initialize the database to store analysis results:

```bash
python database/init_db.py --sample
```

This creates:
- SQLite database at `database/skillsync.db`
- Pre-populated with sample data
- Ready for storing analyses

### Configuration

Streamlit automatically detects `.streamlit/config.toml`:
- Dark theme enabled by default
- Custom colors configured
- Settings applied automatically

### Environment Variables

Optional: Add API keys to `.streamlit/secrets.toml`:
```toml
openai_api_key = "your-key-here"
aws_access_key_id = "your-key-here"
```

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| `pip: command not found` | Install Python 3.8+ from python.org |
| `Module not found` | Run `pip install -r requirements.txt` |
| `Port 8501 in use` | Run `streamlit run app/main.py --server.port 8502` |
| `Resume upload fails` | Ensure file is < 200MB and format is PDF/DOCX/TXT |
| `Streamlit not responsive` | Wait 10 seconds or refresh browser |

## 📁 File Structure

```
Skill gap analyser/
├── app/main.py                    # Dashboard entry point
├── app/pages/                     # 5 analysis pages
├── modules/                       # Analysis modules
├── database/                      # Database setup
├── data/raw/courses.csv           # Course database
├── requirements.txt               # Dependencies
└── pipeline.py                    # Orchestrator
```

## ⚙️ Common Commands

```bash
# Run the app
streamlit run app/main.py

# Run on different port
streamlit run app/main.py --server.port 8502

# Initialize database
python database/init_db.py --sample

# Stop the app
Ctrl + C

# Clear Streamlit cache
streamlit cache clear

# Run in production
streamlit run app/main.py --logger.level=warning
```

## 🎓 Sample Workflow

### Example: Analyzing for "Senior Python Developer"

1. **Upload Resume**
   - Upload your current resume
   - App extracts: Python (90%), SQL (85%), Leadership (80%)

2. **Paste Job Description**
   ```
   Position: Senior Python Developer
   Required: Python, SQL, AWS, Docker, Kubernetes
   ...
   ```

3. **View Results**
   - ATS Score: 78% (Good Match)
   - Matched: Python, SQL
   - Missing: AWS, Docker, Kubernetes
   - Timeline: 6-8 weeks to learn all missing skills

4. **Get Courses**
   - AWS Course: 20 hours, $299
   - Docker Mastery: 17 hours, $14.99
   - Kubernetes Guide: 22 hours, $14.99

5. **Career Path**
   - Senior Python Dev: 85% confidence
   - DevOps Engineer: 72% confidence
   - Tech Lead: 68% confidence

## 💡 Pro Tips

1. **Use Multiple Job Descriptions**
   - Analyze different roles to see where you fit best
   - Identify common skills across roles

2. **Build Your Learning Plan**
   - Add courses to your plan
   - Filter by free vs. paid
   - Start with high-priority skills

3. **Track Progress**
   - Re-run analysis after learning new skills
   - See how your scores improve
   - Export reports for sharing

4. **Leverage Session State**
   - Streamlit remembers your resume within session
   - No need to re-upload
   - Switch between tabs freely

## 🚀 Next Steps

1. ✅ Run the app (see above)
2. 📖 Upload sample resume from `/data/raw/`
3. 📝 Use example job description
4. 🎯 Explore all 5 tabs
5. 📚 Check [README.md](README.md) for detailed documentation

## 📞 Support

- **Stuck?** Check [START_HERE.md](START_HERE.md) for detailed setup
- **Questions?** Read [README.md](README.md) for full documentation
- **Issues?** Check error messages in terminal output

---

**Ready? Run this command:**

```bash
streamlit run app/main.py
```

**Then upload your resume and start analyzing! 🚀**
