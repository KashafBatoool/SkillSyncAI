# WEEK 1 — Step-by-Step Detailed Implementation

## 📅 DAY 1: Project & Environment Setup

### Step 1: Create Project Directory
```bash
# Open PowerShell and run:
mkdir C:\skillsync
cd C:\skillsync
```

### Step 2: Create Virtual Environment
```bash
# In PowerShell (Windows):
python -m venv venv
venv\Scripts\activate

# You should see (venv) in your terminal prefix
```

### Step 3: Create Folder Structure
```bash
# Copy-paste this command (all at once):
mkdir app\pages, app\components, modules, data\raw, data\processed, data\models, notebooks, tests, database
```

**Verify the structure:**
```bash
tree /F  # Shows folder tree in Windows
```

Expected output:
```
C:\SKILLSYNC
    app\
        pages\
        components\
    modules\
    data\
        raw\
        processed\
        models\
    notebooks\
    tests\
    database\
```

---

## 📅 DAY 2: Install Dependencies

### Step 1: Create requirements.txt
Create a file `C:\skillsync\requirements.txt` with this content:

```
# Core
streamlit>=1.32.0
streamlit-extras

# ML/NLP
torch>=2.0.0
transformers>=4.35.0
sentence-transformers>=2.2.2
scikit-learn>=1.3.0
spacy>=3.6.0
nltk>=3.8.0

# Resume Parsing
pdfminer.six>=20221105
python-docx>=1.0.0
PyMuPDF>=1.23.0

# Data
pandas>=2.0.0
numpy>=1.24.0

# Visualization
plotly>=5.17.0
matplotlib>=3.7.0

# Utilities
requests>=2.31.0
python-dotenv>=1.0.0
tqdm>=4.66.0

# Testing
pytest>=7.4.0
```

### Step 2: Install All Packages
```bash
# Make sure you're in C:\skillsync with (venv) activated
pip install -r requirements.txt

# This will take 5-10 minutes. Wait for "Successfully installed..."
```

### Step 3: Download SpaCy English Model
```bash
python -m spacy download en_core_web_sm
```

### Step 4: Download NLTK Data
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### Step 5: Verify Installation
```bash
python -c "import torch, transformers, spacy, streamlit; print('✅ All imports successful!')"
```

---

## 📅 DAY 3: Environment Configuration

### Step 1: Create .env File
Create `C:\skillsync\.env` with this content (fill in values next):

```
# YouTube API
YOUTUBE_API_KEY=your_key_here

# HuggingFace
HUGGINGFACE_API_KEY=your_key_here

# O*NET (optional, for later)
ONET_USERNAME=your_username
ONET_PASSWORD=your_password
```

### Step 2: Get YouTube API Key
1. Go to https://console.cloud.google.com/
2. Click "Create Project" → name it "SkillSync"
3. Search for "YouTube Data API v3" → Enable it
4. Go to "Credentials" → "Create Credential" → API Key
5. Copy key → paste into `.env` file

### Step 3: Get HuggingFace API Key
1. Go to https://huggingface.co/settings/tokens
2. Click "New token" → name it "skillsync"
3. Copy token → paste into `.env` file

### Step 4: Create .gitignore File
Create `C:\skillsync\.gitignore`:

```
venv/
.env
__pycache__/
*.pyc
*.pkl
*.db
data/raw/
data/processed/
data/models/
.DS_Store
.streamlit/secrets.toml
```

### Step 5: Create .streamlit/secrets.toml (for later deployment)
Create file `C:\skillsync\.streamlit\secrets.toml`:

```toml
YOUTUBE_API_KEY = "your_key_here"
HUGGINGFACE_API_KEY = "your_key_here"
```

---

## 📅 DAY 4–5: Data Collection (All Free)

### Step 1: Download O*NET Skills Database

1. Go to https://www.onetcenter.org/developers.html
2. Click "Free Downloads" → Register (free account, research tier)
3. Download `Occupation Data.xlsx`
4. Download `Skills.xlsx`
5. **Place both in `C:\skillsync\data\raw\`**

*Note: You'll convert these to CSV format in Week 2*

### Step 2: Download Kaggle Resume Dataset

1. Go to https://kaggle.com → Create free account
2. Search for `"UpdatedResumeDataSet"` by yushi1990
3. Click Download → Save to `C:\skillsync\data\raw\resumes.csv`

**Alternative if above not available:**
- Search for `"linkedin-job-postings"` by @nicknochnack
- Download the jobs CSV

### Step 3: Download Job Skills Dataset

1. On Kaggle, search for `"job-skills"` or `"linkedin jobs"`
2. Look for CSV with columns: `job_title`, `skills`, `company`, etc.
3. Download → Save to `C:\skillsync\data\raw\job_roles.csv`

### Step 4: Create Courses List (Manually Curated)

Create file `C:\skillsync\data\raw\courses.csv`:

```csv
skill,course_name,platform,url,is_free,duration_hours
Python,Python for Everybody,Coursera,https://www.coursera.org/specializations/python,true,40
Python,Complete Python Bootcamp,Udemy,https://www.udemy.com/course/complete-python-bootcamp,false,22
Python,Python Crash Course Videos,YouTube,https://www.youtube.com/results?search_query=python+crash+course,true,0
JavaScript,The Complete JavaScript Course 2024,Udemy,https://www.udemy.com/course/the-complete-javascript-course-2024,false,69
JavaScript,JavaScript Basics,freeCodeCamp,https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures,true,300
React,React Course - Beginner's Tutorial,freeCodeCamp,https://www.freecodecamp.org/learn/front-end-development-libraries/react,true,50
React,The Complete React Course,Udemy,https://www.udemy.com/course/the-complete-react-guide,false,40
SQL,SQL Tutorial,W3Schools,https://www.w3schools.com/sql,true,0
AWS,AWS Fundamentals,Coursera,https://www.coursera.org/learn/aws-fundamentals-cloud-security,true,30
Docker,Docker for Beginners,Udemy,https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide,false,22
```

### Step 5: Verify All Data Files Exist

```bash
# In PowerShell, check if files exist:
Get-ChildItem C:\skillsync\data\raw\

# You should see:
# - Occupation Data.xlsx (or onet_skills.xlsx)
# - Skills.xlsx
# - resumes.csv
# - job_roles.csv
# - courses.csv
```

---

## 📅 DAY 6: Database Schema Setup

### Step 1: Create Database Schema File

Create file `C:\skillsync\database\schema.sql`:

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Main analysis results
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resume_text TEXT,
    job_role TEXT,
    ats_score REAL,
    extracted_skills TEXT,  -- JSON array
    missing_skills TEXT,    -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Course recommendations
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    course_name TEXT,
    platform TEXT,
    url TEXT,
    skill_covered TEXT,
    relevance_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (analysis_id) REFERENCES analyses(id)
);

-- Career predictions
CREATE TABLE IF NOT EXISTS career_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    career_role TEXT,
    confidence_score REAL,
    matched_skills TEXT,  -- JSON array
    missing_skills TEXT,  -- JSON array
    rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (analysis_id) REFERENCES analyses(id)
);

-- Cache for embeddings (to speed up BERT inference)
CREATE TABLE IF NOT EXISTS embedding_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_hash TEXT UNIQUE,
    embedding TEXT,  -- JSON array of floats
    model_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 2: Initialize the Database

Create file `C:\skillsync\database\init_db.py`:

```python
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'skillsync.db')

def init_database():
    """Create database from schema.sql"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Execute schema
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_database()
```

### Step 3: Run Database Initialization

```bash
# From C:\skillsync directory with (venv) activated:
python database/init_db.py

# Expected output:
# ✅ Database initialized at C:\skillsync\database\skillsync.db
```

### Step 4: Verify Database Created

```bash
# Check if database file exists:
Get-ChildItem C:\skillsync\database\skillsync.db

# Should show the .db file with size > 0
```

---

## 📅 DAY 7: Quick Verification & Checkpoint

### Step 1: Verify Project Structure

```bash
# In PowerShell, display full tree:
tree /F C:\skillsync

# Should show all folders from Day 1 + files created
```

### Step 2: Test All Imports

Create file `C:\skillsync\test_imports.py`:

```python
import sys
print("Python version:", sys.version)

try:
    import streamlit
    print("✅ streamlit")
except: print("❌ streamlit")

try:
    import torch
    print("✅ torch")
except: print("❌ torch")

try:
    import transformers
    print("✅ transformers")
except: print("❌ transformers")

try:
    import sentence_transformers
    print("✅ sentence_transformers")
except: print("❌ sentence_transformers")

try:
    import spacy
    print("✅ spacy")
except: print("❌ spacy")

try:
    import pandas
    print("✅ pandas")
except: print("❌ pandas")

try:
    import sklearn
    print("✅ sklearn")
except: print("❌ sklearn")

try:
    import plotly
    print("✅ plotly")
except: print("❌ plotly")

print("\n✨ All critical packages installed!")
```

### Step 3: Run Verification

```bash
python test_imports.py

# Expected output (all ✅):
# ✅ streamlit
# ✅ torch
# ✅ transformers
# ✅ sentence_transformers
# ✅ spacy
# ✅ pandas
# ✅ sklearn
# ✅ plotly
# ✨ All critical packages installed!
```

### Step 4: Checklist — Week 1 Complete?

- [ ] Virtual environment created and activated
- [ ] All folders created in `C:\skillsync\`
- [ ] `requirements.txt` installed (pip install -r requirements.txt)
- [ ] SpaCy and NLTK models downloaded
- [ ] `.env` file created with API keys
- [ ] O*NET data downloaded to `data/raw/`
- [ ] Resume dataset (Kaggle) in `data/raw/resumes.csv`
- [ ] Job roles dataset in `data/raw/job_roles.csv`
- [ ] Courses list in `data/raw/courses.csv`
- [ ] Database schema created and initialized
- [ ] All imports verified (test_imports.py passed)

---

## 🎯 End of Week 1 Status

✅ **Complete Setup** — Your environment is ready for ML coding
✅ **All Data Downloaded** — No blocking on data collection in Week 2
✅ **Database Ready** — Can store results starting Week 2
✅ **Dependencies Installed** — Zero import errors

**You are now ready to start Week 2: Core AI Modules**

---

## ⚠️ Troubleshooting Common Week 1 Issues

| Problem | Solution |
|---|---|
| `pip install` fails with permission error | Run PowerShell as Administrator |
| Virtual env won't activate | Check: `venv\Scripts\activate` has correct path |
| SpaCy download fails | Run: `python -m spacy download en_core_web_sm --user` |
| Kaggle CSV not found | Ensure free Kaggle account is created and you're logged in |
| `.env` not found error in Week 2 | Ensure file is at: `C:\skillsync\.env` (in root, not in subfolders) |
| Database init fails | Check `schema.sql` is at: `C:\skillsync\database\schema.sql` |

---

*Week 1 Detailed Steps — Ready to proceed? Start with Day 1, Step 1.*
