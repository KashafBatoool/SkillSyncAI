"""
Career Predictor Module - Predict suitable career paths based on skills
Matches current skills against 8 career profiles
"""

from typing import List, Dict
from fuzzywuzzy import fuzz


class CareerPredictor:
    """Predict career paths based on skill profile"""
    
    # Career profiles with required skills
    CAREER_PROFILES = {
        'Backend Developer': {
            'description': 'Focus on server-side development, databases, and APIs',
            'required_skills': ['python', 'java', 'nodejs', 'sql', 'databases', 'api design',
                              'system design', 'microservices', 'docker', 'git'],
            'avg_salary_usd': 120000,
            'growth': 'High',
            'market_demand': 'Very High'
        },
        'Frontend Developer': {
            'description': 'Build user interfaces and web applications',
            'required_skills': ['javascript', 'react', 'vue', 'html', 'css', 'typescript',
                              'responsive design', 'rest api', 'git', 'testing'],
            'avg_salary_usd': 110000,
            'growth': 'High',
            'market_demand': 'Very High'
        },
        'Full Stack Developer': {
            'description': 'Work on both frontend and backend development',
            'required_skills': ['javascript', 'python', 'react', 'nodejs', 'sql', 'html', 'css',
                              'api design', 'databases', 'git', 'docker'],
            'avg_salary_usd': 125000,
            'growth': 'High',
            'market_demand': 'Very High'
        },
        'Data Scientist': {
            'description': 'Extract insights from data using machine learning',
            'required_skills': ['python', 'machine learning', 'data analysis', 'sql', 'statistics',
                              'tensorflow', 'pytorch', 'pandas', 'matplotlib', 'deep learning'],
            'avg_salary_usd': 135000,
            'growth': 'Very High',
            'market_demand': 'Very High'
        },
        'DevOps Engineer': {
            'description': 'Manage infrastructure, deployment, and system operations',
            'required_skills': ['docker', 'kubernetes', 'aws', 'linux', 'jenkins', 'terraform',
                              'ci/cd', 'scripting', 'monitoring', 'networking'],
            'avg_salary_usd': 140000,
            'growth': 'Very High',
            'market_demand': 'High'
        },
        'Cloud Architect': {
            'description': 'Design and manage cloud infrastructure solutions',
            'required_skills': ['aws', 'azure', 'gcp', 'kubernetes', 'system design',
                              'networking', 'security', 'terraform', 'devops', 'microservices'],
            'avg_salary_usd': 150000,
            'growth': 'Very High',
            'market_demand': 'High'
        },
        'Mobile Developer': {
            'description': 'Develop applications for mobile devices',
            'required_skills': ['swift', 'kotlin', 'react native', 'flutter', 'javascript',
                              'ui/ux', 'rest api', 'databases', 'git', 'testing'],
            'avg_salary_usd': 115000,
            'growth': 'High',
            'market_demand': 'High'
        },
        'QA Engineer': {
            'description': 'Ensure software quality through testing and automation',
            'required_skills': ['testing', 'automation', 'selenium', 'jira', 'scripting',
                              'sql', 'api testing', 'ci/cd', 'python', 'problem solving'],
            'avg_salary_usd': 105000,
            'growth': 'Medium',
            'market_demand': 'High'
        },
    }
    
    def __init__(self, fuzzy_threshold: int = 60):
        """Initialize career predictor"""
        self.fuzzy_threshold = fuzzy_threshold
    
    def predict(self, user_skills: List[str], top_n: int = 5) -> List[Dict]:
        """
        Predict suitable career paths
        
        Args:
            user_skills: List of user's current skills
            top_n: Number of top career suggestions
            
        Returns:
            List of career predictions with confidence scores
        """
        user_skills = [s.lower().strip() for s in user_skills]
        career_scores = []
        
        for career_name, profile in self.CAREER_PROFILES.items():
            # Calculate match score
            score = self._calculate_career_score(user_skills, profile['required_skills'])
            
            # Get matched and missing skills
            matched_skills = self._get_matched_skills(user_skills, profile['required_skills'])
            missing_skills = self._get_missing_skills(user_skills, profile['required_skills'])
            
            career_scores.append({
                'career': career_name,
                'confidence': score,
                'description': profile['description'],
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'avg_salary_usd': profile['avg_salary_usd'],
                'growth': profile['growth'],
                'market_demand': profile['market_demand'],
                'required_skills_count': len(profile['required_skills']),
                'matched_count': len(matched_skills)
            })
        
        # Sort by confidence
        career_scores.sort(key=lambda x: x['confidence'], reverse=True)
        
        return career_scores[:top_n]
    
    def _calculate_career_score(self, user_skills: List[str], required_skills: List[str]) -> float:
        """Calculate match score for a career"""
        if not required_skills:
            return 0.0
        
        matched = 0
        for required in required_skills:
            required_lower = required.lower()
            for user_skill in user_skills:
                user_skill_lower = user_skill.lower()
                similarity = fuzz.token_set_ratio(user_skill_lower, required_lower)
                if similarity >= self.fuzzy_threshold:
                    matched += 1
                    break
        
        return (matched / len(required_skills)) * 100
    
    def _get_matched_skills(self, user_skills: List[str], required_skills: List[str]) -> List[str]:
        """Get skills the user has that match the career"""
        matched = []
        
        for user_skill in user_skills:
            user_skill_lower = user_skill.lower()
            for required in required_skills:
                required_lower = required.lower()
                similarity = fuzz.token_set_ratio(user_skill_lower, required_lower)
                if similarity >= self.fuzzy_threshold:
                    matched.append(required)
                    break
        
        return list(set(matched))
    
    def _get_missing_skills(self, user_skills: List[str], required_skills: List[str]) -> List[str]:
        """Get skills needed for the career that user doesn't have"""
        missing = []
        
        for required in required_skills:
            required_lower = required.lower()
            is_matched = False
            
            for user_skill in user_skills:
                user_skill_lower = user_skill.lower()
                similarity = fuzz.token_set_ratio(user_skill_lower, required_lower)
                if similarity >= self.fuzzy_threshold:
                    is_matched = True
                    break
            
            if not is_matched:
                missing.append(required)
        
        return list(set(missing))
    
    def get_career_development_plan(self, career: str, missing_skills: List[str]) -> Dict:
        """Get a development plan for a specific career"""
        if career not in self.CAREER_PROFILES:
            return {}
        
        profile = self.CAREER_PROFILES[career]
        
        # Estimate learning time
        total_hours = len(missing_skills) * 50  # avg 50 hours per skill
        weeks = max(4, int(total_hours / 15))  # assume 15 hours/week
        
        return {
            'career': career,
            'description': profile['description'],
            'current_match_percentage': ((len(profile['required_skills']) - len(missing_skills)) 
                                         / len(profile['required_skills']) * 100),
            'missing_skills': missing_skills[:5],  # Top 5 to learn
            'estimated_learning_hours': total_hours,
            'estimated_weeks': weeks,
            'learning_phases': [
                {
                    'phase': 1,
                    'duration_weeks': max(2, weeks // 3),
                    'focus': 'Fundamentals of missing skills',
                    'skills': missing_skills[:3] if len(missing_skills) > 0 else []
                },
                {
                    'phase': 2,
                    'duration_weeks': max(2, weeks // 3),
                    'focus': 'Intermediate concepts and projects',
                    'skills': missing_skills[3:6] if len(missing_skills) > 3 else []
                },
                {
                    'phase': 3,
                    'duration_weeks': max(2, weeks - 2*(weeks // 3)),
                    'focus': 'Advanced applications and portfolio projects',
                    'skills': []
                }
            ],
            'market_insights': {
                'salary_expectancy': f'${profile["avg_salary_usd"]:,}',
                'growth_rate': profile['growth'],
                'market_demand': profile['market_demand']
            }
        }


# Module-level function for backward compatibility
def predict_careers(user_skills: List[str]) -> List[Dict]:
    """Predict career paths for a user"""
    predictor = CareerPredictor()
    return predictor.predict(user_skills)
