"""
Skill Gap Analysis Page - Display matched/missing/excess skills and learning timeline
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.skill_extractor import SkillExtractor
from modules.gap_analyzer import GapAnalyzer

st.set_page_config(page_title="Skill Gap", page_icon="🎯", layout="wide")

st.title("🎯 Skill Gap Analysis")
st.markdown("Understand your skill gaps and create a learning plan")

# Check if analysis data is available
if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume first on the Resume Analysis page")
    st.stop()

if 'job_description' not in st.session_state or not st.session_state.job_description:
    st.warning("⚠️ Please paste a job description on the Job Matching page")
    st.stop()

# Extract and analyze skills
extractor = SkillExtractor()
resume_skills = set(extractor.extract(st.session_state.resume_text))
job_skills = set(extractor.extract(st.session_state.job_description))

analyzer = GapAnalyzer()
gap_analysis = analyzer.analyze(resume_skills, job_skills)

# Main metrics
st.subheader("📊 Skill Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Your Skills",
        len(resume_skills),
        delta="Total"
    )

with col2:
    st.metric(
        "Job Requirements",
        len(job_skills),
        delta="Total"
    )

with col3:
    matched = len(gap_analysis.get('matched_skills', []))
    st.metric(
        "Matched Skills",
        matched,
        delta=f"{(matched/len(job_skills)*100):.0f}%"
    )

with col4:
    missing = len(gap_analysis.get('missing_skills', []))
    gap_percentage = (missing / len(job_skills) * 100) if job_skills else 0
    st.metric(
        "Skills to Learn",
        missing,
        delta=f"{gap_percentage:.0f}%"
    )

st.markdown("---")

# Skill breakdown visualization
st.subheader("📈 Skill Breakdown")

col1, col2, col3 = st.columns(3)

# Matched skills
with col1:
    matched_skills = gap_analysis.get('matched_skills', [])
    
    st.success(f"✅ **Matched Skills ({len(matched_skills)})**")
    
    if matched_skills:
        st.write(", ".join(matched_skills[:10]))
        if len(matched_skills) > 10:
            st.caption(f"+{len(matched_skills) - 10} more skills")
    else:
        st.info("No matched skills found")

# Missing skills
with col2:
    missing_skills = gap_analysis.get('missing_skills', [])
    
    st.warning(f"❌ **Missing Skills ({len(missing_skills)})**")
    
    if missing_skills:
        st.write(", ".join(missing_skills[:10]))
        if len(missing_skills) > 10:
            st.caption(f"+{len(missing_skills) - 10} more skills")
    else:
        st.success("You have all required skills!")

# Excess skills
with col3:
    excess_skills = gap_analysis.get('excess_skills', [])
    
    st.info(f"➕ **Excess Skills ({len(excess_skills)})**")
    
    if excess_skills:
        st.write(", ".join(excess_skills[:10]))
        if len(excess_skills) > 10:
            st.caption(f"+{len(excess_skills) - 10} more skills")
    else:
        st.info("No excess skills")

st.markdown("---")

# Detailed analysis
st.subheader("📋 Detailed Skills Analysis")

tab1, tab2, tab3 = st.tabs(["Matched ✅", "Missing ❌", "Excess ➕"])

with tab1:
    matched_skills = gap_analysis.get('matched_skills', [])
    if matched_skills:
        st.success(f"**{len(matched_skills)} skills match the job requirements**")
        
        # Organize by category
        technical_matched = [s for s in matched_skills if any(t in s.lower() for t in ['python', 'java', 'sql', 'javascript', 'aws'])]
        soft_matched = [s for s in matched_skills if any(t in s.lower() for t in ['communication', 'leadership', 'teamwork'])]
        other_matched = [s for s in matched_skills if s not in technical_matched and s not in soft_matched]
        
        if technical_matched:
            st.write("**Technical Skills:**")
            for skill in technical_matched:
                st.write(f"  ✅ {skill}")
        
        if soft_matched:
            st.write("**Soft Skills:**")
            for skill in soft_matched:
                st.write(f"  ✅ {skill}")
        
        if other_matched:
            st.write("**Other Skills:**")
            for skill in other_matched[:10]:
                st.write(f"  ✅ {skill}")
    else:
        st.warning("No matched skills found")

with tab2:
    missing_skills = gap_analysis.get('missing_skills', [])
    if missing_skills:
        st.warning(f"**{len(missing_skills)} skills need to be learned**")
        st.write("Priority order (based on frequency in job description):")
        
        # Priority categorization
        high_priority = missing_skills[:min(3, len(missing_skills))]
        medium_priority = missing_skills[3:min(6, len(missing_skills))]
        low_priority = missing_skills[6:]
        
        if high_priority:
            st.error("**🔴 High Priority** (Learn first)")
            for skill in high_priority:
                st.write(f"  1️⃣ {skill}")
        
        if medium_priority:
            st.warning("**🟡 Medium Priority** (Learn next)")
            for skill in medium_priority:
                st.write(f"  2️⃣ {skill}")
        
        if low_priority:
            st.info("**🟢 Low Priority** (Nice to have)")
            for skill in low_priority[:5]:
                st.write(f"  3️⃣ {skill}")
            if len(low_priority) > 5:
                st.caption(f"  ... and {len(low_priority) - 5} more")
    else:
        st.success("No missing skills! You have all requirements")

with tab3:
    excess_skills = gap_analysis.get('excess_skills', [])
    if excess_skills:
        st.info(f"**{len(excess_skills)} extra skills not required**")
        st.write("These are valuable but not explicitly required:")
        for skill in excess_skills[:20]:
            st.write(f"  ➕ {skill}")
        if len(excess_skills) > 20:
            st.caption(f"... and {len(excess_skills) - 20} more")
    else:
        st.info("No excess skills")

st.markdown("---")

# Learning timeline
st.subheader("📅 Recommended Learning Timeline")

missing_skills = gap_analysis.get('missing_skills', [])

if missing_skills:
    # Categorize by difficulty
    high_priority = missing_skills[:min(3, len(missing_skills))]
    medium_priority = missing_skills[3:min(6, len(missing_skills))]
    low_priority = missing_skills[6:]
    
    timeline_data = [
        ("Week 1-2", "🔴 High Priority", high_priority, "Focus on the most critical skills"),
        ("Week 3-4", "🟡 Medium Priority", medium_priority, "Build on foundational knowledge"),
        ("Week 5-8", "🟢 Low Priority", low_priority, "Deepen expertise"),
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Suggested Timeline:**")
        for period, priority, skills, notes in timeline_data:
            with st.expander(f"{period} - {priority}"):
                st.write(f"{notes}")
                if skills:
                    st.write("Skills to focus on:")
                    for skill in skills[:5]:
                        st.write(f"  • {skill}")
                    if len(skills) > 5:
                        st.caption(f"  ... and {len(skills) - 5} more")
    
    with col2:
        st.info("""
        **Timeline Tips:**
        
        - **Week 1-2**: Start with high priority skills
        - **Week 3-4**: Continue with medium priority
        - **Week 5-8**: Master remaining skills
        - **Week 8+**: Project practice and specialization
        
        Adjust based on your:
        - Current learning pace
        - Available time per week
        - Prior knowledge
        """)

else:
    st.success("✅ You already have all the required skills!")

st.markdown("---")

# Priority categorization
st.subheader("🎯 Priority-Based Skill Breakdown")

if missing_skills:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔴 High Priority", len(high_priority) if 'high_priority' in locals() else 0)
    
    with col2:
        st.metric("🟡 Medium Priority", len(medium_priority) if 'medium_priority' in locals() else 0)
    
    with col3:
        st.metric("🟢 Low Priority", len(low_priority) if 'low_priority' in locals() else 0)
else:
    st.success("All skills are already at your level!")

st.markdown("---")

# Action recommendations
st.subheader("💡 Next Steps")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ✅ **What to do next:**
    1. Go to the **Recommendations** page
    2. Find courses for missing skills
    3. Create a learning plan
    """)

with col2:
    st.info("""
    💡 **Pro Tips:**
    - Start with 1-2 skills at a time
    - Use project-based learning
    - Practice on real problems
    - Track your progress
    """)

# Export option
if st.button("📥 Export Gap Analysis", use_container_width=True):
    export_data = {
        "matched_skills": gap_analysis.get('matched_skills', []),
        "missing_skills": gap_analysis.get('missing_skills', []),
        "excess_skills": gap_analysis.get('excess_skills', []),
    }
    st.json(export_data)
    st.success("✅ Analysis exported as JSON")
