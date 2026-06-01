"""
Job Matching Page - Compare resume against job descriptions with ATS scoring
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.ats_scorer import ATSScorer
from modules.skill_extractor import SkillExtractor

st.set_page_config(page_title="Job Matching", page_icon="💼", layout="wide")

st.title("💼 Job Matching")
st.markdown("Paste a job description to see how well your resume matches and get an ATS score")

# Check if resume is uploaded
if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume first on the Resume Analysis page")
    st.stop()

# Job description input
st.subheader("📝 Job Description Input")

job_description = st.text_area(
    "Paste the job description here",
    height=300,
    placeholder="Job Title: \nCompany:\nResponsibilities:\n...",
    help="Paste the complete job description to analyze"
)

if job_description:
    st.session_state.job_description = job_description
    
    # Calculate ATS Score
    if st.button("🎯 Calculate ATS Score", use_container_width=True, type="primary"):
        with st.spinner("Analyzing resume against job description..."):
            try:
                # Calculate ATS score
                scorer = ATSScorer()
                ats_score = scorer.score(st.session_state.resume_text, job_description)
                details = scorer.get_details()
                
                # Display main score
                st.subheader("📊 ATS Score Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("ATS Score", f"{ats_score:.1f}%")
                
                with col2:
                    if ats_score >= 80:
                        status = "🟢 Excellent"
                    elif ats_score >= 60:
                        status = "🟡 Good"
                    elif ats_score >= 40:
                        status = "🟠 Fair"
                    else:
                        status = "🔴 Needs Work"
                    
                    st.metric("Status", status)
                
                with col3:
                    if ats_score >= 75:
                        rec = "✅ Apply Now"
                    elif ats_score >= 50:
                        rec = "⚠️ Prepare First"
                    else:
                        rec = "❌ Not Ready"
                    
                    st.metric("Recommendation", rec)
                
                with col4:
                    gap = 100 - ats_score
                    st.metric("Improvement Needed", f"{gap:.1f}%")
                
                # Score breakdown
                st.subheader("📈 Score Breakdown")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"**Analysis Details:** {details}")
                
                with col2:
                    st.success("""
                    **What ATS Score Means:**
                    - 80-100%: Strong match, likely to pass ATS
                    - 60-79%: Good match, competitive
                    - 40-59%: Fair match, needs improvement
                    - 0-39%: Poor match, needs major changes
                    """)
                
                # Skill comparison
                st.subheader("🎯 Skill Comparison")
                
                extractor = SkillExtractor()
                resume_skills = set(extractor.extract(st.session_state.resume_text))
                job_skills = set(extractor.extract(job_description))
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    matched = resume_skills & job_skills
                    st.metric("Matched Skills", len(matched))
                    if matched:
                        st.caption(", ".join(list(matched)[:5]))
                
                with col2:
                    missing = job_skills - resume_skills
                    st.metric("Missing Skills", len(missing))
                    if missing:
                        st.caption(", ".join(list(missing)[:5]))
                
                with col3:
                    excess = resume_skills - job_skills
                    st.metric("Excess Skills", len(excess))
                    if excess:
                        st.caption(", ".join(list(excess)[:5]))
                
                # Detailed skill analysis
                st.subheader("📋 Detailed Skill Analysis")
                
                tab1, tab2, tab3 = st.tabs(["Matched Skills ✅", "Missing Skills ❌", "Excess Skills ➕"])
                
                with tab1:
                    if matched:
                        st.success(f"You have {len(matched)} of the required skills:")
                        for skill in sorted(matched):
                            st.write(f"• {skill}")
                    else:
                        st.warning("No matching skills found")
                
                with tab2:
                    if missing:
                        st.warning(f"You're missing {len(missing)} skills that are in the job description:")
                        for skill in sorted(missing):
                            st.write(f"• {skill}")
                        
                        st.markdown("---")
                        st.info("💡 These are the skills you should focus on learning to improve your match!")
                    else:
                        st.success("You have all the required skills!")
                
                with tab3:
                    if excess:
                        st.info(f"You have {len(excess)} additional skills not listed in the job description:")
                        for skill in sorted(excess)[:10]:
                            st.write(f"• {skill}")
                        if len(excess) > 10:
                            st.caption(f"... and {len(excess) - 10} more")
                    else:
                        st.info("No excess skills")
                
                # Keywords analysis
                st.subheader("🔍 Keyword Matching")
                
                common_keywords = []
                resume_lower = st.session_state.resume_text.lower()
                job_lower = job_description.lower()
                
                # Check for common technical keywords
                keywords = ['python', 'java', 'sql', 'aws', 'agile', 'git', 'docker', 'kubernetes', 'react', 'angular']
                for keyword in keywords:
                    if keyword in resume_lower and keyword in job_lower:
                        common_keywords.append(keyword)
                
                if common_keywords:
                    st.success(f"Found {len(common_keywords)} common keywords: {', '.join(common_keywords)}")
                else:
                    st.info("No common technical keywords detected")
                
                # Recommendations
                st.subheader("💡 Recommendations")
                
                if ats_score >= 75:
                    st.success("""
                    ✅ **Your resume looks great for this position!**
                    - Your skills closely match the job requirements
                    - Consider applying immediately
                    - You may want to customize your cover letter to highlight matched skills
                    """)
                elif ats_score >= 50:
                    st.warning(f"""
                    ⚠️ **Good match, but needs some work**
                    - You're missing {len(missing)} key skills
                    - Consider updating your resume to highlight relevant experiences
                    - Learn or highlight the missing skills before applying
                    """)
                else:
                    st.error(f"""
                    ❌ **Not a strong match yet**
                    - You're missing {len(missing)} key skills
                    - Consider skipping this role or upskilling first
                    - Use the Recommendations page to find learning resources for missing skills
                    """)
                
                # Save results
                if st.button("💾 Save Job Match Results", use_container_width=True):
                    st.session_state.last_ats_score = ats_score
                    st.session_state.last_job_analysis = {
                        'score': ats_score,
                        'matched_skills': list(matched),
                        'missing_skills': list(missing),
                        'excess_skills': list(excess)
                    }
                    st.success("✅ Results saved to session!")
                
            except Exception as e:
                st.error(f"Error calculating ATS score: {str(e)}")
                st.info("Try pasting a different job description or check your resume format")

else:
    st.info("👆 Paste a job description above to get started")
    
    # Example job description
    with st.expander("📋 Example Job Description"):
        st.code("""
Position: Senior Python Developer
Company: Tech Corp

About the Role:
We're looking for an experienced Python developer to join our growing team. You'll be responsible for developing and maintaining our core backend services, working with our talented engineering team.

Key Responsibilities:
- Design and develop scalable Python applications
- Collaborate with cross-functional teams
- Write clean, maintainable code with comprehensive testing
- Participate in code reviews and mentoring

Required Qualifications:
- 5+ years of Python development experience
- Strong knowledge of SQL and database design
- Experience with AWS and cloud services
- Familiarity with Git and Agile methodologies
- Excellent problem-solving and communication skills

Nice to Have:
- Docker and Kubernetes experience
- Experience with microservices architecture
- Knowledge of Machine Learning frameworks
        """, language="text")

with st.expander("📚 Understanding ATS Scores"):
    st.write("""
    An **ATS (Applicant Tracking System) Score** measures how well your resume matches a job description:
    
    - **80-100%**: Excellent match - Your resume has most/all required keywords and skills
    - **60-79%**: Good match - Your resume has many relevant skills and keywords
    - **40-59%**: Fair match - Your resume has some relevant content but is missing key elements
    - **0-39%**: Poor match - Your resume lacks many required skills or keywords
    
    **Tips to improve your ATS score:**
    1. Use keywords from the job description in your resume
    2. Match the format and structure of the job posting
    3. Include specific technical skills mentioned in the description
    4. Tailor your resume for each application
    5. Use standard section headers (Experience, Skills, Education)
    """)
