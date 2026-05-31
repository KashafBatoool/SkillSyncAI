"""
LLM Explainer Module - Generate natural language explanations
Provides human-readable insights about analysis results
"""

from typing import Dict, List


class LLMExplainer:
    """Generate natural language explanations for analysis results"""
    
    def explain_skill_gap(self, gap_analysis: Dict) -> str:
        """Explain skill gaps in human-readable format"""
        match_pct = gap_analysis['match_percentage']
        matched = gap_analysis['matched_count']
        total = gap_analysis['total_job_skills']
        missing = gap_analysis['missing_count']
        
        if match_pct >= 80:
            overall = "🟢 Excellent - You're well-prepared for this role!"
        elif match_pct >= 60:
            overall = "🟡 Good - You have most of the required skills"
        elif match_pct >= 40:
            overall = "🟠 Moderate - Consider developing key skills"
        else:
            overall = "🔴 Low - Significant skill development needed"
        
        explanation = f"""
SKILL MATCH ANALYSIS
{overall}

📊 Overall Match: {match_pct}% ({matched}/{total} skills matched)

Key Findings:
• You have {matched} of {total} required skills
• {missing} critical skills need development
• Learning path estimated at {gap_analysis['learning_roadmap'][0]['phase'] if gap_analysis['learning_roadmap'] else '?'} phases
        
Top Skills to Develop:
"""
        
        for i, skill in enumerate(gap_analysis['missing'][:5], 1):
            explanation += f"\n{i}. {skill['skill'].upper()}"
            explanation += f"\n   └─ Priority: {skill['priority']} | Learning: ~{skill['learning_hours']} hours"
        
        return explanation
    
    def explain_ats_score(self, ats_result: Dict) -> str:
        """Explain ATS score"""
        score = ats_result['ats_score']
        breakdown = ats_result['breakdown']
        keywords = ats_result['matched_keywords'][:5]
        
        if score >= 80:
            interpretation = "✅ EXCELLENT - Your resume should pass most ATS systems!"
        elif score >= 70:
            interpretation = "✓ GOOD - Strong resume that should perform well with ATS"
        elif score >= 50:
            interpretation = "⚠ MODERATE - Consider improving keyword usage"
        else:
            interpretation = "❌ LOW - Significant improvements needed"
        
        explanation = f"""
ATS COMPATIBILITY SCORE
{interpretation}

📈 Overall Score: {score}/100

Score Breakdown:
• Semantic Similarity: {breakdown['bert_similarity']}/100 (how well your resume matches the job)
• Keyword Alignment: {breakdown['tfidf_similarity']}/100 (proper terminology use)
• Required Keywords: {breakdown['keyword_match']}/100 (presence of must-have skills)

Top Matched Keywords:
{', '.join(keywords) if keywords else 'None'}

Recommendations:
• Ensure job title and key skills appear in your resume
• Use specific technical terminology from job posting
• Organize information in standard sections
        """
        
        return explanation
    
    def explain_career_match(self, career_predictions: List[Dict]) -> str:
        """Explain career predictions"""
        if not career_predictions:
            return "No career predictions available."
        
        top_career = career_predictions[0]
        confidence = top_career['confidence']
        matched = top_career['matched_count']
        required = top_career['required_skills_count']
        missing = required - matched
        
        explanation = f"""
CAREER PATH RECOMMENDATIONS

🎯 Top Recommended: {top_career['career'].upper()}
Confidence: {confidence:.1f}%

{top_career['description']}

Your Profile Match:
• You have {matched}/{required} required skills ({(matched/required*100):.0f}%)
• Skills to develop: {missing}
• Time to proficiency: ~{missing * 8} weeks (10-15 hours/week)

Why This Career?
"""
        
        # Add matched skills explanation
        if top_career['matched_skills']:
            explanation += f"\n✓ You Already Have: {', '.join(top_career['matched_skills'][:3])}"
        
        if top_career['missing_skills']:
            explanation += f"\n• Next Steps: Learn {', '.join(top_career['missing_skills'][:3])}"
        
        # Add market insights
        explanation += f"""

Market Insights:
• Average Salary: ${top_career.get('avg_salary_usd', 'N/A'):,}
• Growth Rate: {top_career.get('growth', 'N/A')}
• Market Demand: {top_career.get('market_demand', 'N/A')}

Other Suitable Careers:
"""
        
        for i, career in enumerate(career_predictions[1:4], 1):
            explanation += f"\n{i}. {career['career']} ({career['confidence']:.0f}% match)"
        
        return explanation
    
    def explain_learning_resource(self, course: Dict) -> str:
        """Explain a specific learning resource"""
        explanation = f"""
COURSE RECOMMENDATION

📚 {course.get('course_name', 'Course')}
Platform: {course.get('platform', 'Unknown')}
Skill: {course.get('skill', 'General').upper()}

Details:
• Duration: {course.get('duration_hours', '?')} hours
• Cost: {'Free' if course.get('is_free') else 'Paid'}
• Relevance: {(course.get('relevance_score', 0) * 100):.0f}%
• Priority: {course.get('priority', 'Medium')}

Why This Course:
This course will help you master {course.get('skill', 'the skill')}, which is
crucial for your career development. The structured curriculum and
{'' if not course.get('is_free') else 'free access make it '}accessible for continuous learning.

What You'll Learn:
• Fundamentals and best practices
• Real-world applications and projects
• Industry-standard tools and workflows
• Hands-on experience with practical exercises
        """
        
        if course.get('url'):
            explanation += f"\nEnroll Now: {course.get('url')}"
        
        return explanation
    
    def generate_comprehensive_report(self, analysis_results: Dict) -> str:
        """Generate a comprehensive analysis report"""
        report = """
╔════════════════════════════════════════════════════════════════════════════╗
║                   SkillSync AI - COMPREHENSIVE ANALYSIS REPORT             ║
╚════════════════════════════════════════════════════════════════════════════╝

1. RESUME ANALYSIS
───────────────────────────────────────────────────────────────────────────
"""
        
        if 'ats_score' in analysis_results:
            ats = analysis_results['ats_score']
            report += f"ATS Score: {ats['ats_score']}/100\n"
        
        report += """
2. SKILL ASSESSMENT
───────────────────────────────────────────────────────────────────────────
"""
        
        if 'gap_analysis' in analysis_results:
            gap = analysis_results['gap_analysis']
            report += f"Match Percentage: {gap['match_percentage']}%\n"
            report += f"Matched Skills: {gap['matched_count']}/{gap['total_job_skills']}\n"
            report += f"Skills to Develop: {gap['missing_count']}\n"
        
        report += """
3. CAREER PATH RECOMMENDATION
───────────────────────────────────────────────────────────────────────────
"""
        
        if 'career_predictions' in analysis_results:
            careers = analysis_results['career_predictions']
            if careers:
                top = careers[0]
                report += f"Recommended Role: {top['career']} ({top['confidence']:.0f}% match)\n"
        
        report += """
4. LEARNING ROADMAP
───────────────────────────────────────────────────────────────────────────
"""
        
        if 'recommended_courses' in analysis_results:
            courses = analysis_results['recommended_courses'][:3]
            for i, course in enumerate(courses, 1):
                report += f"{i}. {course.get('course_name', 'Course')} "
                report += f"({course.get('duration_hours', '?')} hours)\n"
        
        report += """
5. ACTION PLAN
───────────────────────────────────────────────────────────────────────────
Week 1-2: Review fundamentals of top missing skills
Week 3-4: Complete first course module
Week 5-8: Engage in practical projects
Week 9-12: Build portfolio projects
Ongoing: Practice and continuous learning

═════════════════════════════════════════════════════════════════════════════

Generated by SkillSync AI Career Assistant
For more details, visit each recommendation section above.
        """
        
        return report


# Module-level functions for backward compatibility
def explain_gap(gap_analysis: Dict) -> str:
    """Explain skill gap analysis"""
    explainer = LLMExplainer()
    return explainer.explain_skill_gap(gap_analysis)

def explain_ats(ats_result: Dict) -> str:
    """Explain ATS score"""
    explainer = LLMExplainer()
    return explainer.explain_ats_score(ats_result)

def explain_career(career_predictions: List[Dict]) -> str:
    """Explain career predictions"""
    explainer = LLMExplainer()
    return explainer.explain_career_match(career_predictions)
