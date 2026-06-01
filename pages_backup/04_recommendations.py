"""
Recommendations Page - Show course recommendations and learning paths
"""
import streamlit as st
import sys
from pathlib import Path
import csv

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.skill_extractor import SkillExtractor
from modules.gap_analyzer import GapAnalyzer
from modules.recommender import Recommender

st.set_page_config(page_title="Recommendations", page_icon="📚", layout="wide")

st.title("📚 Learning Recommendations")
st.markdown("Discover courses and resources to bridge your skill gaps")

# Check if analysis data is available
if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume first on the Resume Analysis page")
    st.stop()

if 'job_description' not in st.session_state or not st.session_state.job_description:
    st.warning("⚠️ Please paste a job description on the Job Matching page")
    st.stop()

# Get skill gap data
extractor = SkillExtractor()
resume_skills = set(extractor.extract(st.session_state.resume_text))
job_skills = set(extractor.extract(st.session_state.job_description))

analyzer = GapAnalyzer()
gap_analysis = analyzer.analyze(resume_skills, job_skills)

missing_skills = gap_analysis.get('missing_skills', [])

# Get recommendations
recommender = Recommender()
recommendations = recommender.get_recommendations(
    skills_to_learn=missing_skills,
    current_level='beginner'
)

st.subheader("🎯 Missing Skills to Learn")
if missing_skills:
    st.write(", ".join(missing_skills[:10]))
    if len(missing_skills) > 10:
        st.caption(f"... and {len(missing_skills) - 10} more")
else:
    st.success("No missing skills! You're all set!")

st.markdown("---")

# Filters
st.subheader("🔍 Filter Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    platforms = list(set(r.get('platform', 'Other') for r in recommendations)) + ['All']
    selected_platform = st.selectbox(
        "Platform",
        sorted(['All'] + [p for p in platforms if p != 'All'])
    )

with col2:
    price_options = ['All', 'Free', 'Paid']
    selected_price = st.selectbox("Cost", price_options)

with col3:
    levels = ['All', 'Beginner', 'Intermediate', 'Advanced']
    selected_level = st.selectbox("Level", levels)

# Filter recommendations
filtered_recs = recommendations

if selected_platform != 'All':
    filtered_recs = [r for r in filtered_recs if r.get('platform', 'Other') == selected_platform]

if selected_price != 'All':
    filtered_recs = [r for r in filtered_recs 
                     if (selected_price == 'Free' and r.get('price', 0) == 0) or 
                        (selected_price == 'Paid' and r.get('price', 0) > 0)]

if selected_level != 'All':
    filtered_recs = [r for r in filtered_recs if r.get('level', 'Beginner') == selected_level]

st.markdown("---")

# Display recommendations
st.subheader(f"📖 Recommended Courses ({len(filtered_recs)})")

if filtered_recs:
    # Sort by rating (descending)
    filtered_recs = sorted(filtered_recs, key=lambda x: x.get('rating', 0), reverse=True)
    
    for i, course in enumerate(filtered_recs, 1):
        with st.expander(
            f"**{i}. {course.get('title', 'Course')}** - {course.get('platform', 'Unknown')} "
            f"| {course.get('level', 'All')} | ⭐ {course.get('rating', 0)}"
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Description:** {course.get('description', 'N/A')}")
                st.write(f"**Skills Taught:** {', '.join(course.get('skills', [])[:5])}")
                st.write(f"**Duration:** {course.get('duration', 'N/A')}")
                st.write(f"**Cost:** ${course.get('price', 0):.2f}")
            
            with col2:
                st.metric("Rating", f"{course.get('rating', 0):.1f}", delta="⭐")
                
                if course.get('url'):
                    st.markdown(f"[🔗 View Course]({course['url']})")
                
                if st.button(f"⭐ Add to Learning Plan", key=f"course_{i}"):
                    if 'learning_plan' not in st.session_state:
                        st.session_state.learning_plan = []
                    
                    st.session_state.learning_plan.append(course)
                    st.success("✅ Added to learning plan!")
else:
    st.info("No courses match your filters. Try adjusting them.")

st.markdown("---")

# Learning paths
st.subheader("🛣️ Structured Learning Paths")

paths = {
    "Python Developer": [
        "Python Basics",
        "Object-Oriented Programming",
        "Data Structures & Algorithms",
        "Web Development with Django",
        "Advanced Python"
    ],
    "Web Developer": [
        "HTML & CSS",
        "JavaScript Fundamentals",
        "React.js",
        "Node.js & Express",
        "Full Stack Development"
    ],
    "Data Scientist": [
        "Python for Data Science",
        "SQL & Databases",
        "Statistics & Probability",
        "Machine Learning",
        "Deep Learning"
    ],
    "Cloud Engineer": [
        "Cloud Computing Basics",
        "AWS Fundamentals",
        "Infrastructure as Code",
        "Containerization (Docker)",
        "Kubernetes & Orchestration"
    ]
}

selected_path = st.selectbox("Choose a Learning Path", list(paths.keys()))

if selected_path:
    st.write(f"**{selected_path} - Recommended Learning Order:**")
    
    for i, step in enumerate(paths[selected_path], 1):
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.write(f"**Step {i}**")
        
        with col2:
            st.write(step)
            if st.button(f"Find courses for {step}", key=f"path_{selected_path}_{i}"):
                st.info(f"🔍 Searching courses for: {step}")

st.markdown("---")

# Learning plan
st.subheader("📋 Your Learning Plan")

if 'learning_plan' in st.session_state and st.session_state.learning_plan:
    st.success(f"✅ {len(st.session_state.learning_plan)} courses in your plan")
    
    total_cost = sum(c.get('price', 0) for c in st.session_state.learning_plan)
    total_hours = sum(
        float(c.get('duration', '10').split()[0]) 
        if c.get('duration') else 10 
        for c in st.session_state.learning_plan
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Courses", len(st.session_state.learning_plan))
    
    with col2:
        st.metric("Total Cost", f"${total_cost:.2f}")
    
    with col3:
        st.metric("Hours", f"{total_hours:.0f}")
    
    st.write("**Your Courses:**")
    for i, course in enumerate(st.session_state.learning_plan, 1):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"{i}. {course.get('title', 'Course')} - {course.get('platform', 'Unknown')}")
        
        with col2:
            if st.button("❌ Remove", key=f"remove_{i}"):
                st.session_state.learning_plan.pop(i - 1)
                st.rerun()
    
    # Export plan
    if st.button("📥 Export Learning Plan", use_container_width=True):
        export_text = f"""
LEARNING PLAN
Generated on: {st.session_state.get('analysis_date', 'Today')}

Total Courses: {len(st.session_state.learning_plan)}
Total Cost: ${total_cost:.2f}
Estimated Hours: {total_hours:.0f}

COURSES:
"""
        for i, course in enumerate(st.session_state.learning_plan, 1):
            export_text += f"""
{i}. {course.get('title', 'Course')}
   Platform: {course.get('platform', 'Unknown')}
   Cost: ${course.get('price', 0):.2f}
   Duration: {course.get('duration', 'N/A')}
   Level: {course.get('level', 'N/A')}
   URL: {course.get('url', 'N/A')}
"""
        st.download_button(
            label="📥 Download Plan",
            data=export_text,
            file_name="learning_plan.txt",
            mime="text/plain"
        )

else:
    st.info("👆 Add courses to your learning plan to get started")

st.markdown("---")

# Resources
st.subheader("📚 Additional Learning Resources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Popular Platforms:**
    - Coursera
    - Udacity
    - Pluralsight
    - LinkedIn Learning
    - Udemy
    """)

with col2:
    st.markdown("""
    **Free Resources:**
    - YouTube
    - GitHub
    - Documentation
    - Stack Overflow
    - Dev.to
    """)

st.markdown("---")

# Recommendations summary
st.subheader("💡 Recommendations Summary")

st.info(f"""
Based on your skill gap analysis:
- **Missing Skills:** {len(missing_skills)}
- **Recommended Courses:** {len(recommendations)}
- **Avg. Cost per Course:** ${sum(r.get('price', 0) for r in recommendations) / max(len(recommendations), 1):.2f}
- **Avg. Duration:** {sum(float(r.get('duration', '10').split()[0]) for r in recommendations if r.get('duration')) / max(len(recommendations), 1):.0f} hours

Start with high-priority skills and build your expertise progressively.
""")
