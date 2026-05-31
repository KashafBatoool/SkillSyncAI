# 🚀 START HERE - SkillSync Setup Guide

Welcome to **SkillSync** - Your intelligent career development platform!

This guide will get you up and running in **5 minutes**.

## ⚡ Quick Start (For the Impatient)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database (optional)
python database/init_db.py --sample

# 3. Run the app
streamlit run app/main.py

# 4. Open your browser
# The app will open automatically at http://localhost:8501
```

Done! 🎉

## 📋 What is SkillSync?

SkillSync is a comprehensive career development platform that helps you:

- 📄 **Analyze Your Resume** - Extract skills and experience
- 💼 **Match Jobs** - Get ATS scores and match analysis
- 🎯 **Identify Gaps** - See what skills you're missing
- 📚 **Get Recommendations** - Discover courses to bridge gaps
- 🔮 **Predict Career Path** - Understand your growth opportunities

## 🛠️ Prerequisites

Before starting, make sure you have:

- **Python 3.8+** installed ([Download Python](https://www.python.org/downloads/))
- **pip** (comes with Python)
- A text editor or IDE (VS Code, PyCharm, etc.)

## 📦 Installation Steps

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd "Skill gap analyser"

# If downloaded as zip, just extract and navigate to the folder
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected packages to install:
- streamlit
- pandas
- numpy
- scikit-learn
- python-docx
- PyPDF2
- requests

### Step 4: Set Up Configuration (Optional)

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in any API keys you want to use:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

## 🚀 Running the Application

### Start the Streamlit App

```bash
streamlit run app/main.py
```

The app will:
1. Print output in the terminal
2. Automatically open in your default browser at `http://localhost:8501`
3. Show a notification when ready

### Stop the App

Press `Ctrl+C` in the terminal to stop the server.

## 📖 Using SkillSync

### The 5-Step Workflow:

1. **Resume Analysis** (`📄` tab)
   - Upload your resume (PDF, DOCX, or TXT)
   - View extracted information and skills
   - Save the analysis

2. **Job Matching** (`💼` tab)
   - Paste a job description
   - Get ATS score and match analysis
   - See skill comparison

3. **Skill Gap** (`🎯` tab)
   - View matched/missing/excess skills
   - See learning timeline
   - Understand priorities

4. **Recommendations** (`📚` tab)
   - Browse recommended courses
   - Filter by platform and cost
   - Build your learning plan

5. **Career Prediction** (`🔮` tab)
   - Discover career opportunities
   - See development recommendations
   - Plan your growth

## 🗂️ Project Structure

```
Skill gap analyser/
├── app/
│   ├── main.py                    # Main dashboard
│   └── pages/
│       ├── 01_resume_analysis.py
│       ├── 02_job_matching.py
│       ├── 03_skill_gap.py
│       ├── 04_recommendations.py
│       └── 05_career_prediction.py
├── modules/
│   ├── resume_parser.py           # Parse resumes
│   ├── skill_extractor.py         # Extract skills
│   ├── ats_scorer.py              # Calculate ATS score
│   ├── gap_analyzer.py            # Analyze gaps
│   ├── recommender.py             # Recommend courses
│   ├── career_predictor.py        # Predict careers
│   └── llm_explainer.py           # AI explanations
├── database/
│   ├── init_db.py                 # Database setup
│   └── schema.sql                 # Database schema
├── data/
│   └── raw/
│       └── courses.csv            # Course database
├── .streamlit/
│   ├── config.toml                # Streamlit config
│   └── secrets.toml               # API keys
├── pipeline.py                    # Main orchestrator
├── requirements.txt               # Dependencies
└── README.md                      # Full documentation
```

## 🔧 Troubleshooting

### Issue: Module not found errors

**Solution**: Make sure you're in the project directory and have installed all requirements:
```bash
pip install -r requirements.txt
```

### Issue: Port 8501 already in use

**Solution**: Use a different port:
```bash
streamlit run app/main.py --server.port 8502
```

### Issue: File upload not working

**Solution**: Check file permissions and ensure:
- File is < 200MB
- File format is PDF, DOCX, or TXT
- File path doesn't have special characters

### Issue: Database errors

**Solution**: Reinitialize the database:
```bash
python database/init_db.py --reset
```

## 📚 Next Steps

- Read the [QUICKSTART.md](QUICKSTART.md) for advanced features
- Check [README.md](README.md) for complete documentation
- Review [WEEK_1_DETAILED_STEPS.md](WEEK_1_DETAILED_STEPS.md) for learning path

## 🆘 Getting Help

1. **Check Documentation** - Read README.md and guides in `/files/` folder
2. **Review Error Messages** - Streamlit shows detailed error messages
3. **Check Logs** - Terminal output shows application logs
4. **Test with Sample Data** - Use example files in `/data/raw/`

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review code comments in the modules
- Check Streamlit documentation: https://docs.streamlit.io

## ✅ Verification Checklist

Before using SkillSync, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (pip list shows streamlit, pandas, etc.)
- [ ] Project files are in place
- [ ] `.streamlit/config.toml` exists
- [ ] Database initialized (optional but recommended)
- [ ] App starts without errors (streamlit run app/main.py)

## 🎓 Learning Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Python Guide**: https://www.python.org/doc/
- **Pandas Tutorial**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/

---

**Ready to analyze your career? Start with:** `streamlit run app/main.py`

Happy learning! 🚀
