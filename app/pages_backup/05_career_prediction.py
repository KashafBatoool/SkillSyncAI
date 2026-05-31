"""
Career Prediction Page - Display career matches and development plans
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.resume_parser import ResumeParser
from modules.skill_extractor import SkillExtractor
from modules.career_predictor import CareerPredictor

st.set_page_config(page_title="Career Prediction", page_icon="🔮", layout="wide")

st.title("🔮 Career Prediction & Opportunities")
st.markdown("Discover potential career paths and growth opportunities based on your profile")

# Check if resume is uploaded
if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume first on the Resume Analysis page")
    st.stop()

# Parse resume for career prediction
parser = ResumeParser()
parsed_resume = parser.parse(st.session_state.resume_text)

# Extract skills
extractor = SkillExtractor()
current_skills = extractor.extract(st.session_state.resume_text)

# Get career predictions
predictor = CareerPredictor()
career_predictions = predictor.predict(
    current_skills=current_skills,
    experience_level=parsed_resume.get('experience_level', 'beginner'),
    years_experience=parsed_resume.get('years_experience', 0)
)

# Current profile
st.subheader("👤 Your Current Profile")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Current Title", parsed_resume.get('title', 'Unknown'))

with col2:
    st.metric("Experience Level", parsed_resume.get('experience_level', 'N/A').title())

with col3:
    st.metric("Years of Experience", f"{parsed_resume.get('years_experience', 0)} years")

with col4:
    st.metric("Current Skills", len(current_skills))

st.markdown("---")

# Career predictions
st.subheader("🎯 Predicted Career Paths")

if career_predictions:
    # Sort by confidence
    sorted_careers = sorted(career_predictions, key=lambda x: x.get('confidence', 0), reverse=True)
    
    # Top 3 matches
    st.write("### Top Career Matches")
    
    col1, col2, col3 = st.columns(3)
    
    for i, (col, career) in enumerate(zip([col1, col2, col3], sorted_careers[:3])):
        with col:
            confidence = career.get('confidence', 0)
            
            # Color code based on confidence
            if confidence >= 80:
                color = "🟢"
            elif confidence >= 60:
                color = "🟡"
            else:
                color = "🟠"
            
            st.metric(
                f"{color} {career.get('title', 'Unknown')}",
                f"{confidence:.0f}%",
                delta="Confidence"
            )
    
    st.markdown("---")
    
    # Detailed career information
    st.write("### Career Opportunities")
    
    tabs = st.tabs([f"{c.get('title', 'Career')}" for c in sorted_careers[:5]])
    
    for tab, career in zip(tabs, sorted_careers[:5]):
        with tab:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Confidence Score:** {career.get('confidence', 0):.1f}%")
                st.write(f"**Description:** {career.get('description', 'N/A')}")
                
                # Required skills
                required_skills = career.get('required_skills', [])
                if required_skills:
                    st.write("**Required Skills:**")
                    for skill in required_skills:
                        if skill in current_skills:
                            st.write(f"  ✅ {skill}")
                        else:
                            st.write(f"  ❌ {skill}")
                
                # Career path
                career_path = career.get('career_path', [])
                if career_path:
                    st.write("**Typical Career Path:**")
                    for i, step in enumerate(career_path, 1):
                        st.write(f"  {i}. {step}")
            
            with col2:
                st.write("**Key Metrics:**")
                st.metric("Salary Range", career.get('salary_range', 'N/A'))
                st.metric("Job Market", career.get('market_demand', 'High'))
                st.metric("Growth Rate", career.get('growth_rate', 'N/A'))
                
                if st.button("📊 View Details", key=f"details_{career.get('title', 'unknown')}"):
                    st.success("Detailed view opened!")

else:
    st.info("No career predictions available. Please check your resume.")

st.markdown("---")

# Development recommendations
st.subheader("📈 Development Recommendations")

if sorted_careers:
    top_career = sorted_careers[0]
    gap_skills = [s for s in top_career.get('required_skills', []) if s not in current_skills]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"**Target Role: {top_career.get('title', 'Unknown')}**")
        st.write(f"Current Match: {top_career.get('confidence', 0):.0f}%")
        st.write(f"Years to Target: {top_career.get('years_to_reach', 3)}")
    
    with col2:
        if gap_skills:
            st.warning(f"**Skills to Develop:**")
            for skill in gap_skills[:5]:
                st.write(f"  • {skill}")
            if len(gap_skills) > 5:
                st.write(f"  ... and {len(gap_skills) - 5} more")
        else:
            st.success("✅ You have all the required skills!")

st.markdown("---")

# Career progression timeline
st.subheader("📅 Career Progression Timeline")

current_exp = parsed_resume.get('years_experience', 0)

progression_stages = [
    ("Junior", "0-2 years", "🟢"),
    ("Mid-Level", "2-5 years", "🟡"),
    ("Senior", "5-10 years", "🟠"),
    ("Lead/Principal", "10+ years", "🔴"),
]

timeline_col1, timeline_col2 = st.columns([1, 2])

with timeline_col1:
    st.write("**Experience Level:**")
    for stage, years, emoji in progression_stages:
        if stage.lower() == parsed_resume.get('experience_level', 'beginner').lower():
            st.write(f"{emoji} **{stage}** ← You are here")
        else:
            st.write(f"{emoji} {stage}")

with timeline_col2:
    st.write("**Projected Growth:**")
    
    growth_data = [
        ("1-2 years", "Solidify current skills, take on leadership tasks"),
        ("3-5 years", "Develop specialized expertise"),
        ("5-10 years", "Position for senior roles"),
        ("10+ years", "Lead teams, strategic roles"),
    ]
    
    for period, action in growth_data:
        with st.expander(f"📍 {period}"):
            st.write(action)

st.markdown("---")

# Skills development matrix
st.subheader("🎯 Skills Development Matrix")

# Compare current skills with top 3 career paths
top_3_careers = sorted_careers[:3]

st.write("**Skill Requirements by Career Path:**")

# Create comparison
skill_matrix_data = {}

for career in top_3_careers:
    career_title = career.get('title', 'Unknown')
    required = set(career.get('required_skills', []))
    have = required & set(current_skills)
    missing = required - set(current_skills)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**{career_title}**")
    
    with col2:
        st.metric("Match", f"{len(have)}/{len(required)}")
    
    with col3:
        gap_percentage = (len(have) / len(required) * 100) if required else 0
        st.metric("Progress", f"{gap_percentage:.0f}%")

st.markdown("---")

# Action plan
st.subheader("✅ Your Action Plan")

st.write("""
Based on your profile and target roles, here's what you should do:

1. **Immediate (Next 3 months)**
   - Deepen expertise in your strongest skills
   - Start learning top 2-3 missing skills
   - Take on more challenging projects

2. **Short-term (3-6 months)**
   - Complete courses for missing skills
   - Build projects using new technologies
   - Network with professionals in target roles

3. **Medium-term (6-12 months)**
   - Apply for roles with slightly higher requirements
   - Gain practical experience in target domain
   - Mentor junior team members

4. **Long-term (1-2 years)**
   - Position yourself for promotion/role change
   - Develop leadership skills
   - Build personal brand in your field
""")

# Comparison with similar roles
st.subheader("🔄 Similar Roles You Might Consider")

if sorted_careers and len(sorted_careers) > 1:
    st.write("Based on your current skills, you might also be a good fit for:")
    
    for career in sorted_careers[1:4]:
        match_score = career.get('confidence', 0)
        st.write(f"**{career.get('title', 'Unknown')}** - {match_score:.0f}% match")

# Export career plan
st.markdown("---")

if st.button("📥 Export Career Plan", use_container_width=True):
    export_text = f"""
CAREER DEVELOPMENT PLAN
Generated: Today

CURRENT PROFILE
===============
Title: {parsed_resume.get('title', 'Unknown')}
Experience Level: {parsed_resume.get('experience_level', 'N/A')}
Years of Experience: {parsed_resume.get('years_experience', 0)}
Current Skills: {len(current_skills)}

TARGET ROLES (Top 3)
===================
"""
    
    for i, career in enumerate(sorted_careers[:3], 1):
        export_text += f"""
{i}. {career.get('title', 'Unknown')}
   Confidence: {career.get('confidence', 0):.0f}%
   Salary Range: {career.get('salary_range', 'N/A')}
   Description: {career.get('description', 'N/A')}
"""
    
    st.download_button(
        label="📥 Download Plan",
        data=export_text,
        file_name="career_plan.txt",
        mime="text/plain"
    )
    st.success("✅ Career plan ready for download!")
