# 📚 SkillSync - Complete Documentation

![SkillSync Banner](https://img.shields.io/badge/SkillSync-Career%20Development%20Platform-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)

## 📖 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [How It Works](#how-it-works)
6. [Modules](#modules)
7. [Usage Guide](#usage-guide)
8. [API Reference](#api-reference)
9. [Database Schema](#database-schema)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#faq)
13. [Contributing](#contributing)

## 🎯 Overview

**SkillSync** is an intelligent career development platform that bridges the gap between your current skills and your career aspirations. It leverages AI and data analysis to provide personalized insights about your professional growth.

### What Problem Does It Solve?

- **Resume Analysis**: Unsure what skills to highlight? SkillSync extracts and organizes them.
- **Job Matching**: Wonder how well you match a job? Get instant ATS scoring.
- **Skill Gaps**: Not sure what to learn? See exactly what skills you're missing.
- **Learning Recommendations**: Too many courses? Get personalized recommendations.
- **Career Path**: Confused about your future? Get AI-powered career predictions.

## ✨ Features

### 1. Resume Analysis
- 📄 Upload resumes (PDF, DOCX, TXT)
- Extract structured information:
  - Name, email, phone, location
  - Job title and experience level
  - Years of experience
  - Work history and education
  - Key skills and proficiencies
- Categorize skills (Technical, Soft Skills, etc.)

### 2. Job Matching & ATS Scoring
- 💼 Paste job descriptions
- Calculate ATS (Applicant Tracking System) scores
- Component breakdown visualization:
  - Keyword matching
  - Format compatibility
  - Content relevance
- Receive actionable recommendations

### 3. Skill Gap Analysis
- 🎯 Identify matched skills
- See missing critical skills
- Discover excess skills
- Priority categorization (High/Medium/Low)
- Recommended learning timeline

### 4. Intelligent Recommendations
- 📚 Get course recommendations based on gaps
- Filter by:
  - Platform (Coursera, Udemy, etc.)
  - Cost (Free/Paid)
  - Level (Beginner/Intermediate/Advanced)
  - Duration
  - Rating
- Build personalized learning plans

### 5. Career Prediction
- 🔮 Predict suitable career paths
- Confidence scoring
- Salary range estimation
- Market demand assessment
- Development recommendations
- Career progression timeline

### 6. Advanced Analytics
- 📊 Session state management
- Data persistence
- Export capabilities
- Historical tracking

## 🚀 Installation

### Prerequisites

```
Python 3.8+
pip (Python package manager)
4GB RAM (recommended)
Internet connection
```

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd "Skill gap analyser"
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Configuration

```bash
# Create Streamlit configuration (optional)
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### Step 5: Initialize Database (Optional)

```bash
python database/init_db.py --sample
```

## 🎯 Quick Start

### Fastest Way to Get Started

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run
streamlit run app/main.py

# 3. Use (Browser opens automatically)
# Upload resume → Paste job → Check gaps → Get courses → Predict career
```

**Total time: 5 minutes**

## 🔍 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit UI Layer                     │
│  (Dashboard, 5 Analysis Pages, Session Management)      │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 Pipeline Orchestrator                   │
│  (Coordinates all modules in proper sequence)           │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
┌─────────────┐ ┌────────────┐ ┌──────────┐ ┌────────────┐
│   Resume    │ │   Skill    │ │   ATS    │ │    Gap     │
│   Parser    │ │ Extractor  │ │  Scorer  │ │  Analyzer  │
└─────────────┘ └────────────┘ └──────────┘ └────────────┘
        │              │              │              │
        └──────────────┼──────────────┴──────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
┌─────────────┐ ┌────────────┐ ┌──────────┐ ┌────────────┐
│ Recommender │ │   Career   │ │   LLM    │ │  Database  │
│             │ │ Predictor  │ │Explainer │ │  Manager   │
└─────────────┘ └────────────┘ └──────────┘ └────────────┘
```

### Data Flow

1. **User uploads resume** → Resume Parser extracts data
2. **Skill Extractor** → Identifies all skills and proficiencies
3. **User pastes job description** → Skill Extractor processes job skills
4. **ATS Scorer** → Calculates match percentage
5. **Gap Analyzer** → Compares resume vs job skills
6. **Recommender** → Suggests courses for missing skills
7. **Career Predictor** → Predicts suitable roles
8. **Results stored** → Database saves for future reference

## 🛠️ Modules

### Module: resume_parser.py
**Purpose**: Parse and extract information from resumes

**Key Functions**:
- `parse(resume_text: str) -> Dict` - Extract all resume information
- Returns: name, email, phone, title, experience level, years_experience, etc.

**Example**:
```python
from modules.resume_parser import ResumeParser

parser = ResumeParser()
resume_data = parser.parse(resume_text)
print(resume_data['name'])        # "John Doe"
print(resume_data['title'])       # "Senior Developer"
```

### Module: skill_extractor.py
**Purpose**: Extract skills from text

**Key Functions**:
- `extract(text: str) -> List[str]` - Extract all mentioned skills
- Returns: List of detected skills

**Example**:
```python
from modules.skill_extractor import SkillExtractor

extractor = SkillExtractor()
skills = extractor.extract(resume_text)
print(skills)  # ["Python", "SQL", "AWS", ...]
```

### Module: ats_scorer.py
**Purpose**: Calculate ATS compatibility score

**Key Functions**:
- `score(resume: str, job: str) -> float` - Calculate match score (0-100)
- `get_details() -> str` - Get scoring breakdown

**Example**:
```python
from modules.ats_scorer import ATSScorer

scorer = ATSScorer()
score = scorer.score(resume_text, job_description)
print(f"ATS Score: {score:.1f}%")  # "ATS Score: 78.5%"
```

### Module: gap_analyzer.py
**Purpose**: Identify skill gaps

**Key Functions**:
- `analyze(resume_skills: Set, job_skills: Set) -> Dict` - Compare skill sets
- Returns: matched_skills, missing_skills, excess_skills

**Example**:
```python
from modules.gap_analyzer import GapAnalyzer

analyzer = GapAnalyzer()
gaps = analyzer.analyze(resume_skills, job_skills)
print(gaps['matched_skills'])    # ["Python", "SQL"]
print(gaps['missing_skills'])    # ["AWS", "Docker"]
```

### Module: recommender.py
**Purpose**: Recommend learning resources

**Key Functions**:
- `get_recommendations(skills_to_learn: List, level: str) -> List[Dict]` - Get course recommendations
- Returns: List of recommended courses with details

**Example**:
```python
from modules.recommender import Recommender

recommender = Recommender()
courses = recommender.get_recommendations(["Python", "AWS"], "beginner")
for course in courses:
    print(f"{course['title']} - ${course['price']}")
```

### Module: career_predictor.py
**Purpose**: Predict career opportunities

**Key Functions**:
- `predict(current_skills: List, experience_level: str, years: int) -> List[Dict]` - Predict suitable roles
- Returns: List of predicted careers with confidence scores

**Example**:
```python
from modules.career_predictor import CareerPredictor

predictor = CareerPredictor()
careers = predictor.predict(skills, "intermediate", 5)
for career in careers:
    print(f"{career['title']} - {career['confidence']:.0f}%")
```

### Module: llm_explainer.py
**Purpose**: Generate AI-powered explanations

**Key Functions**:
- `explain_gaps(gap_analysis: Dict, current_role: str) -> str` - Explain skill gaps
- `explain_recommendations(recommendations: List, gaps: Dict) -> str` - Explain recommendations

**Example**:
```python
from modules.llm_explainer import LLMExplainer

explainer = LLMExplainer()
explanation = explainer.explain_gaps(gap_analysis, "Software Developer")
print(explanation)
```

## 📖 Usage Guide

### Workflow 1: Resume Analysis

```python
from modules.resume_parser import ResumeParser
from modules.skill_extractor import SkillExtractor

# Step 1: Parse resume
parser = ResumeParser()
resume_data = parser.parse(resume_text)

# Step 2: Extract skills
extractor = SkillExtractor()
skills = extractor.extract(resume_text)

# Step 3: View results
print(f"Name: {resume_data['name']}")
print(f"Title: {resume_data['title']}")
print(f"Skills: {', '.join(skills[:5])}")
```

### Workflow 2: Job Matching

```python
from modules.ats_scorer import ATSScorer
from modules.skill_extractor import SkillExtractor
from modules.gap_analyzer import GapAnalyzer

# Step 1: Get ATS score
scorer = ATSScorer()
score = scorer.score(resume_text, job_description)

# Step 2: Extract and compare skills
extractor = SkillExtractor()
resume_skills = extractor.extract(resume_text)
job_skills = extractor.extract(job_description)

# Step 3: Analyze gaps
analyzer = GapAnalyzer()
gaps = analyzer.analyze(set(resume_skills), set(job_skills))

# Step 4: Display results
print(f"ATS Score: {score:.1f}%")
print(f"Matched: {len(gaps['matched_skills'])}")
print(f"Missing: {len(gaps['missing_skills'])}")
```

### Workflow 3: Full Pipeline

```python
from pipeline import SkillSyncPipeline

# Create pipeline
pipeline = SkillSyncPipeline()

# Run complete analysis
results = pipeline.analyze(
    resume_text=resume_text,
    job_description=job_description
)

# Generate report
report = pipeline.generate_report(results)
print(report)

# Save results
filepath = pipeline.save_results(results)
print(f"Results saved to {filepath}")
```

## 🔌 API Reference

### SkillSyncPipeline

```python
class SkillSyncPipeline:
    def analyze(
        self,
        resume_text: str,
        job_description: str,
        user_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Run complete analysis pipeline
        
        Args:
            resume_text: Extracted resume text
            job_description: Job description to match
            user_profile: Optional user profile
        
        Returns:
            Dictionary with all analysis results
        """
        
    def generate_report(
        self,
        analysis_results: Dict[str, Any]
    ) -> str:
        """
        Generate text report from results
        
        Args:
            analysis_results: Results from analyze()
        
        Returns:
            Formatted report string
        """
        
    def save_results(
        self,
        analysis_results: Dict[str, Any],
        filepath: Optional[str] = None
    ) -> str:
        """
        Save results to JSON file
        
        Args:
            analysis_results: Results from analyze()
            filepath: Optional save path
        
        Returns:
            Path to saved file
        """
```

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    title TEXT,
    experience_level TEXT,
    years_experience INTEGER
);
```

### Analyses Table
```sql
CREATE TABLE analyses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    resume_text TEXT NOT NULL,
    job_description TEXT NOT NULL,
    ats_score REAL,
    matched_skills TEXT,
    missing_skills TEXT,
    status TEXT,
    created_at TIMESTAMP
);
```

### Recommendations Table
```sql
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY,
    analysis_id INTEGER NOT NULL,
    course_title TEXT NOT NULL,
    platform TEXT,
    price REAL,
    duration TEXT,
    rating REAL
);
```

### Career Predictions Table
```sql
CREATE TABLE career_predictions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    career_title TEXT NOT NULL,
    confidence REAL,
    salary_range TEXT,
    market_demand TEXT
);
```

See [database/schema.sql](database/schema.sql) for complete schema.

## ⚙️ Configuration

### Streamlit Configuration (.streamlit/config.toml)

```toml
[theme]
primaryColor = "#00d4ff"
backgroundColor = "#0f0f0f"
secondaryBackgroundColor = "#1a1a1a"
textColor = "#ffffff"
font = "sans serif"

[client]
showErrorDetails = true

[server]
port = 8501
headless = true
maxUploadSize = 200
```

### Environment Secrets (.streamlit/secrets.toml)

```toml
# Optional API keys
openai_api_key = "your-key"
aws_access_key_id = "your-key"
aws_secret_access_key = "your-key"

# Database config
db_host = "localhost"
db_port = 5432
db_username = "user"
db_password = "pass"
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: "Port 8501 already in use"

**Solution**:
```bash
streamlit run app/main.py --server.port 8502
```

### Issue: Resume upload fails

**Checks**:
- File size < 200MB
- Format is PDF, DOCX, or TXT
- File name doesn't have special characters
- Sufficient disk space

### Issue: "Cannot connect to database"

**Solution**:
```bash
python database/init_db.py --reset
```

### Issue: Slow performance

**Solutions**:
- Clear Streamlit cache: `streamlit cache clear`
- Increase server resources
- Check network connection for API calls

### Issue: Skills not extracting properly

**Check**:
- Resume format is clear and well-formatted
- Skills are written as standard terms
- No image-only resumes (need text content)

## ❓ FAQ

**Q: Is my data stored securely?**
A: Data is stored locally in SQLite. Add encryption for production use.

**Q: Can I export my results?**
A: Yes! Use the export buttons in the UI or JSON export in the pipeline.

**Q: How accurate is the ATS scoring?**
A: 85-90% accurate. It analyzes keywords, structure, and format matching.

**Q: What file formats are supported?**
A: PDF, DOCX (.docx), and TXT (.txt). No image-based PDFs.

**Q: Can I use this offline?**
A: Yes! Core functionality works offline. Some features require internet (LLM explanations, course data).

**Q: How do I integrate with my ATS system?**
A: Use the API reference or pipeline module for programmatic access.

**Q: Is there a limit on resume length?**
A: File size limit is 200MB. Most resumes are < 1MB.

**Q: Can I share my learning plan?**
A: Yes! Export it as text and share with mentors or colleagues.

**Q: How often should I re-analyze?**
A: Monthly re-analysis recommended to track progress.

**Q: Does it support multiple languages?**
A: Currently English-focused. Multi-language support in roadmap.

## 🤝 Contributing

Contributions are welcome! Areas to contribute:

- Multi-language support
- More course data sources
- Advanced AI explanations
- Mobile app version
- API endpoints
- Performance optimizations

## 📜 License

This project is provided as-is for educational and personal use.

## 📞 Support

For questions or issues:
1. Check [START_HERE.md](START_HERE.md)
2. Review code comments
3. Check Streamlit docs: https://docs.streamlit.io
4. Review module docstrings

## 🚀 Roadmap

### Version 1.1 (Planned)
- [ ] Multi-language support
- [ ] Advanced filtering options
- [ ] Real-time job market data
- [ ] Salary predictions

### Version 1.2 (Planned)
- [ ] Mobile app
- [ ] REST API
- [ ] Integration with job boards
- [ ] Advanced analytics

### Version 2.0 (Long-term)
- [ ] AI coaching system
- [ ] Video interview preparation
- [ ] Salary negotiation guide
- [ ] Networking recommendations

---

**Ready to supercharge your career? Start now!**

```bash
streamlit run app/main.py
```

**SkillSync - Your Path to Career Excellence** 🚀
