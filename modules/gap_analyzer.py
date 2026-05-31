"""
Gap Analyzer Module - Analyze skill gaps between resume and job requirements
Provides prioritized list of missing skills with learning time estimates
"""

from typing import List, Dict
from fuzzywuzzy import fuzz
import re


class GapAnalyzer:
    """Analyze skill gaps between current and required skills"""
    
    # Learning time estimates by skill type (hours)
    LEARNING_TIME_ESTIMATES = {
        'language': {'easy': 40, 'medium': 80, 'hard': 200},
        'framework': {'easy': 30, 'medium': 60, 'hard': 150},
        'tool': {'easy': 20, 'medium': 40, 'hard': 100},
        'methodology': {'easy': 10, 'medium': 20, 'hard': 50},
    }
    
    # Skill difficulty levels
    SKILL_DIFFICULTY = {
        # Easy skills
        'easy': ['git', 'linux', 'html', 'css', 'bash', 'sql basics'],
        # Medium skills
        'medium': ['python', 'javascript', 'react', 'docker', 'aws', 'testing'],
        # Hard skills
        'hard': ['kubernetes', 'tensorflow', 'apache spark', 'machine learning', 'deep learning'],
    }
    
    def __init__(self, fuzzy_threshold: int = 70):
        """Initialize gap analyzer with improved threshold of 70 for better accuracy"""
        self.fuzzy_threshold = fuzzy_threshold
    
    def analyze(
        self,
        resume_skills: List[str],
        job_skills: List[str]
    ) -> Dict:
        """
        Analyze skill gaps
        
        Args:
            resume_skills: List of skills from resume
            job_skills: List of skills from job description
            
        Returns:
            Dict with matched, missing, excess, and statistics
        """
        # Normalize skills
        resume_skills = [s.lower().strip() for s in resume_skills]
        job_skills = [s.lower().strip() for s in job_skills]
        
        # Find matches
        matched = self._find_matches(resume_skills, job_skills)
        
        # Find missing skills
        missing = self._find_missing(job_skills, resume_skills)
        
        # Find excess skills (in resume but not in job)
        excess = self._find_excess(resume_skills, job_skills)
        
        # Prioritize missing skills
        prioritized_missing = self._prioritize_missing(missing)
        
        # Calculate statistics
        total_job_skills = len(job_skills)
        match_percentage = (len(matched) / total_job_skills * 100) if total_job_skills > 0 else 0
        
        return {
            'matched': matched,
            'missing': prioritized_missing,
            'excess': excess,
            'match_percentage': round(match_percentage, 1),
            'matched_count': len(matched),
            'missing_count': len(missing),
            'total_job_skills': total_job_skills,
            'learning_roadmap': self._generate_learning_roadmap(prioritized_missing)
        }
    
    def _find_matches(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """Find matching skills between resume and job"""
        matched = []
        
        for job_skill in job_skills:
            for resume_skill in resume_skills:
                similarity = fuzz.token_set_ratio(job_skill, resume_skill)
                if similarity >= self.fuzzy_threshold:
                    matched.append(job_skill)
                    break
        
        return list(set(matched))
    
    def _find_missing(self, job_skills: List[str], resume_skills: List[str]) -> List[str]:
        """Find skills in job that are not in resume"""
        missing = []
        
        for job_skill in job_skills:
            is_matched = False
            for resume_skill in resume_skills:
                similarity = fuzz.token_set_ratio(job_skill, resume_skill)
                if similarity >= self.fuzzy_threshold:
                    is_matched = True
                    break
            
            if not is_matched:
                missing.append(job_skill)
        
        return list(set(missing))
    
    def _find_excess(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """Find skills in resume not required by job"""
        excess = []
        
        for resume_skill in resume_skills:
            is_matched = False
            for job_skill in job_skills:
                similarity = fuzz.token_set_ratio(resume_skill, job_skill)
                if similarity >= self.fuzzy_threshold:
                    is_matched = True
                    break
            
            if not is_matched:
                excess.append(resume_skill)
        
        return list(set(excess))
    
    def _prioritize_missing(self, missing_skills: List[str]) -> List[Dict]:
        """Prioritize missing skills (High, Medium, Low)"""
        prioritized = []
        
        # Core/High priority skills
        high_priority_keywords = ['senior', 'lead', 'architect', 'system', 'principal', 'required']
        
        for skill in missing_skills:
            priority = 'Medium'
            learning_time = self._estimate_learning_time(skill)
            
            # Determine priority
            if any(keyword in skill.lower() for keyword in high_priority_keywords):
                priority = 'High'
            elif learning_time < 50:
                priority = 'Low'
            
            prioritized.append({
                'skill': skill,
                'priority': priority,
                'learning_hours': learning_time,
                'difficulty': self._get_difficulty_level(skill)
            })
        
        # Sort by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        prioritized.sort(key=lambda x: (priority_order.get(x['priority'], 3), x['learning_hours']))
        
        return prioritized
    
    def _estimate_learning_time(self, skill: str) -> int:
        """Estimate learning time for a skill (hours)"""
        skill_lower = skill.lower()
        
        # Identify skill type
        skill_type = 'tool'  # default
        
        if any(lang in skill_lower for lang in ['python', 'javascript', 'java', 'c#', 'go', 'rust']):
            skill_type = 'language'
        elif any(fw in skill_lower for fw in ['react', 'django', 'spring', 'vue', 'angular']):
            skill_type = 'framework'
        elif any(method in skill_lower for method in ['agile', 'scrum', 'kanban']):
            skill_type = 'methodology'
        
        # Determine difficulty
        difficulty = self._get_difficulty_level(skill)
        
        # Get estimate
        estimates = self.LEARNING_TIME_ESTIMATES.get(skill_type, {'easy': 25, 'medium': 50, 'hard': 100})
        return estimates.get(difficulty, 50)
    
    def _get_difficulty_level(self, skill: str) -> str:
        """Get difficulty level of a skill"""
        skill_lower = skill.lower()
        
        for level, skills in self.SKILL_DIFFICULTY.items():
            if any(s in skill_lower for s in skills):
                return level
        
        return 'medium'  # default
    
    def _generate_learning_roadmap(self, prioritized_missing: List[Dict]) -> List[Dict]:
        """Generate a learning roadmap for missing skills"""
        roadmap = []
        
        # Group by priority
        by_priority = {'High': [], 'Medium': [], 'Low': []}
        for skill_info in prioritized_missing:
            by_priority[skill_info['priority']].append(skill_info)
        
        # Phase 1: High priority skills (should take 2-4 weeks)
        phase_1_hours = 0
        for skill_info in by_priority['High'][:5]:  # Max 5 high priority
            roadmap.append({
                'phase': 1,
                'skill': skill_info['skill'],
                'hours': skill_info['learning_hours'],
                'duration_weeks': max(1, skill_info['learning_hours'] // 15)
            })
            phase_1_hours += skill_info['learning_hours']
        
        # Phase 2: Medium priority skills (2-4 weeks)
        for skill_info in by_priority['Medium'][:5]:
            roadmap.append({
                'phase': 2,
                'skill': skill_info['skill'],
                'hours': skill_info['learning_hours'],
                'duration_weeks': max(1, skill_info['learning_hours'] // 15)
            })
        
        # Phase 3: Low priority and nice-to-have
        for skill_info in by_priority['Low'][:3]:
            roadmap.append({
                'phase': 3,
                'skill': skill_info['skill'],
                'hours': skill_info['learning_hours'],
                'duration_weeks': max(1, skill_info['learning_hours'] // 15)
            })
        
        return roadmap
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate human-readable gap analysis report"""
        report = f"""
Skill Gap Analysis Report
=========================
Overall Match: {analysis['match_percentage']}%
- Matched Skills: {analysis['matched_count']} / {analysis['total_job_skills']}
- Missing Skills: {analysis['missing_count']}
- Extra Skills: {len(analysis['excess'])}

Top 5 Missing Skills (Priority Order):
"""
        for i, skill in enumerate(analysis['missing'][:5], 1):
            report += f"\n{i}. {skill['skill']}"
            report += f"\n   Priority: {skill['priority']} | Learning Time: ~{skill['learning_hours']} hours"
        
        return report


# Module-level function for backward compatibility
def analyze_gap(resume_skills: List[str], job_skills: List[str]) -> Dict:
    """Analyze skill gap between resume and job"""
    analyzer = GapAnalyzer()
    return analyzer.analyze(resume_skills, job_skills)
