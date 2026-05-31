"""
SkillSync - Simple Test App
Quick test to verify Streamlit is working
"""
import streamlit as st

st.set_page_config(page_title="SkillSync", page_icon="🚀")

st.title("🚀 SkillSync AI Resume Analyzer")
st.subheader("Welcome to Your AI-Powered Career Assistant")

st.markdown("""
## ✅ Streamlit is Working!

Your SkillSync application is running successfully on **http://localhost:8501**

### 📋 Features Available:
- 📄 Resume Parsing (PDF, DOCX, TXT)
- 🎯 Skill Gap Analysis
- 💼 ATS Score Calculation
- 🎓 Course Recommendations
- 🚀 Career Path Prediction

---

### 🚀 Quick Start:
1. Upload your resume
2. Paste a job description  
3. Get instant AI insights

### 📊 Project Status: ✅ READY
""")

st.success("✨ Application loaded successfully!")
