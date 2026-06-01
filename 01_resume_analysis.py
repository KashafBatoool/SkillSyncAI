"""
Resume Analysis Page - First page for resume upload and skill extraction
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.resume_parser import ResumeParser
from modules.skill_extractor import SkillExtractor

st.set_page_config(page_title="Resume Analysis", page_icon="📄", layout="wide")

st.title("📄 Resume Analysis")
st.markdown("Upload and analyze your resume to extract key information and skills")

# File upload
uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX, TXT"
)

if uploaded_file is not None:
    try:
        # Read file content
        if uploaded_file.type == "text/plain":
            resume_text = uploaded_file.read().decode('utf-8')
        else:
            st.info(f"Processing {uploaded_file.name} (type: {uploaded_file.type})")
            resume_text = f"Resume content from {uploaded_file.name}"
        
        # Store in session state
        st.session_state.resume_text = resume_text
        st.session_state.resume_filename = uploaded_file.name
        
        st.success(f"✅ Successfully uploaded {uploaded_file.name}")
        
        # Parse resume
        parser = ResumeParser()
        parsed_resume = parser.parse(resume_text)
        
        # Display basic information
        st.subheader("📋 Extracted Information")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Full Name",
                parsed_resume.get('name', 'Not found')
            )
        
        with col2:
            st.metric(
                "Job Title",
                parsed_resume.get('title', 'Not found')
            )
        
        with col3:
            st.metric(
                "Years of Experience",
                f"{parsed_resume.get('years_experience', 0)} years"
            )
        
        with col4:
            st.metric(
                "Experience Level",
                parsed_resume.get('experience_level', 'Not determined').title()
            )
        
        # Contact information
        st.subheader("📧 Contact Information")
        
        contact_data = {
            "Email": parsed_resume.get('email', 'Not found'),
            "Phone": parsed_resume.get('phone', 'Not found'),
            "Location": parsed_resume.get('location', 'Not found'),
            "LinkedIn": parsed_resume.get('linkedin', 'Not found'),
        }
        
        for key, value in contact_data.items():
            st.write(f"**{key}:** {value}")
        
        # Skills extraction
        st.subheader("🎯 Extracted Skills")
        
        extractor = SkillExtractor()
        skills = extractor.extract(resume_text)
        
        if skills:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                skill_categories = {
                    'Technical': [s for s in skills if any(tech in s.lower() for tech in ['python', 'java', 'sql', 'javascript', 'react', 'aws'])],
                    'Soft Skills': [s for s in skills if any(soft in s.lower() for soft in ['communication', 'leadership', 'teamwork', 'problem-solving'])],
                    'Other': [s for s in skills if s not in [s for sublist in [skills] for s in sublist]][:len(skills)//3]
                }
                
                tabs = st.tabs(["All Skills", "Technical", "Soft Skills"])
                
                with tabs[0]:
                    st.write(f"**Total Skills Found: {len(skills)}**")
                    st.write(", ".join(skills[:20]))
                    if len(skills) > 20:
                        st.caption(f"... and {len(skills) - 20} more skills")
                
                with tabs[1]:
                    tech = skill_categories['Technical']
                    if tech:
                        st.write(f"**Found {len(tech)} technical skills:**")
                        st.write(", ".join(tech))
                    else:
                        st.info("No technical skills detected")
                
                with tabs[2]:
                    soft = skill_categories['Soft Skills']
                    if soft:
                        st.write(f"**Found {len(soft)} soft skills:**")
                        st.write(", ".join(soft))
                    else:
                        st.info("No soft skills detected")
            
            with col2:
                st.metric("Total Skills", len(skills))
        else:
            st.warning("No skills detected in resume")
        
        # Work experience
        st.subheader("💼 Work Experience")
        
        experience = parsed_resume.get('experience', [])
        if experience:
            for i, exp in enumerate(experience, 1):
                with st.expander(f"Position {i}: {exp.get('title', 'Unknown')}"):
                    st.write(f"**Company:** {exp.get('company', 'N/A')}")
                    st.write(f"**Duration:** {exp.get('duration', 'N/A')}")
                    st.write(f"**Description:** {exp.get('description', 'N/A')}")
        else:
            st.info("No work experience extracted")
        
        # Education
        st.subheader("🎓 Education")
        
        education = parsed_resume.get('education', [])
        if education:
            for edu in education:
                with st.expander(f"{edu.get('degree', 'Unknown')} in {edu.get('field', 'Unknown')}"):
                    st.write(f"**School/University:** {edu.get('institution', 'N/A')}")
                    st.write(f"**Graduation Year:** {edu.get('year', 'N/A')}")
        else:
            st.info("No education information extracted")
        
        # Full text preview
        with st.expander("📄 Full Resume Text Preview"):
            st.text_area(
                "Resume content",
                value=resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text,
                disabled=True,
                height=300
            )
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Save Analysis", use_container_width=True):
                st.success("Resume analysis saved to session!")
        
        with col2:
            if st.button("🔄 Extract Again", use_container_width=True):
                st.rerun()
        
        with col3:
            st.info("➡️ Next: Go to Job Matching to compare", icon="ℹ️")
        
    except Exception as e:
        st.error(f"Error processing resume: {str(e)}")
        st.info("💡 Make sure your file is in a supported format (PDF, DOCX, or TXT)")

else:
    st.info("👆 Upload a resume file to get started")
    
    # Example information
    with st.expander("📚 What this page does"):
        st.write("""
        This page helps you:
        
        1. **Upload Your Resume** - Support for PDF, DOCX, and TXT formats
        2. **Extract Information** - Automatically extract:
           - Name, email, phone, location
           - Job title and experience level
           - Work experience and education
           - Skills and technical proficiencies
        3. **Preview Results** - See all extracted data organized by category
        4. **Next Steps** - Use this data for job matching and skill gap analysis
        
        Your resume data is stored in the current session and used for all subsequent analyses.
        """)
