"""
Recommender Module - Recommend courses for missing skills
Supports multiple platforms: Coursera, Udemy, freeCodeCamp
"""

import csv
from pathlib import Path
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Recommender:
    """Recommend learning resources for skill gaps"""
    
    # Dummy courses for when CSV is not available
    DUMMY_COURSES = [
        {
            'title': 'Python for Everybody',
            'platform': 'Coursera',
            'url': 'https://coursera.org/python',
            'price': 0,
            'duration': '40 hours',
            'level': 'Beginner',
            'rating': 4.7,
            'description': 'Learn Python programming from scratch.',
            'skills': ['python'],
        },
        {
            'title': 'JavaScript Complete Course',
            'platform': 'Udemy',
            'url': 'https://udemy.com/javascript',
            'price': 14.99,
            'duration': '30 hours',
            'level': 'Beginner',
            'rating': 4.5,
            'description': 'Master JavaScript fundamentals and modern syntax.',
            'skills': ['javascript'],
        },
        {
            'title': 'React - The Complete Guide',
            'platform': 'Udemy',
            'url': 'https://udemy.com/react',
            'price': 14.99,
            'duration': '25 hours',
            'level': 'Intermediate',
            'rating': 4.6,
            'description': 'Build modern React applications from scratch.',
            'skills': ['react'],
        },
        {
            'title': 'Docker Mastery',
            'platform': 'Udemy',
            'url': 'https://udemy.com/docker',
            'price': 14.99,
            'duration': '20 hours',
            'level': 'Intermediate',
            'rating': 4.7,
            'description': 'Learn Docker containerization and deployment.',
            'skills': ['docker'],
        },
        {
            'title': 'Kubernetes for Developers',
            'platform': 'Coursera',
            'url': 'https://coursera.org/kubernetes',
            'price': 49,
            'duration': '30 hours',
            'level': 'Intermediate',
            'rating': 4.6,
            'description': 'Deploy and scale apps on Kubernetes.',
            'skills': ['kubernetes'],
        },
        {
            'title': 'Machine Learning Specialization',
            'platform': 'Coursera',
            'url': 'https://coursera.org/ml',
            'price': 0,
            'duration': '60 hours',
            'level': 'Intermediate',
            'rating': 4.7,
            'description': 'Core machine learning concepts and practice.',
            'skills': ['machine learning'],
        },
        {
            'title': 'AWS Solutions Architect',
            'platform': 'Udemy',
            'url': 'https://udemy.com/aws',
            'price': 14.99,
            'duration': '40 hours',
            'level': 'Intermediate',
            'rating': 4.6,
            'description': 'Prepare for the AWS Solutions Architect exam.',
            'skills': ['aws'],
        },
        {
            'title': 'Git Complete',
            'platform': 'freeCodeCamp',
            'url': 'https://freecodecamp.org/git',
            'price': 0,
            'duration': '8 hours',
            'level': 'Beginner',
            'rating': 4.4,
            'description': 'Version control essentials with Git.',
            'skills': ['git'],
        },
        {
            'title': 'SQL for Data Analysis',
            'platform': 'Coursera',
            'url': 'https://coursera.org/sql',
            'price': 49,
            'duration': '20 hours',
            'level': 'Beginner',
            'rating': 4.5,
            'description': 'Learn SQL for analytics and reporting.',
            'skills': ['sql'],
        },
        {
            'title': 'MongoDB Complete',
            'platform': 'Udemy',
            'url': 'https://udemy.com/mongodb',
            'price': 14.99,
            'duration': '15 hours',
            'level': 'Beginner',
            'rating': 4.4,
            'description': 'Master MongoDB basics and best practices.',
            'skills': ['mongodb'],
        },
    ]

    
    def __init__(self, courses_csv_path: str = 'data/raw/courses.csv'):
        """Initialize recommender
        
        Args:
            courses_csv_path: Path to courses CSV file
        """
        self.courses_csv_path = courses_csv_path
        self.courses = self._load_courses()
    
    def _load_courses(self) -> List[Dict]:
        """Load courses from CSV file"""
        courses = []
        csv_path = Path(self.courses_csv_path)
        
        if csv_path.exists():
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        courses.append(self._normalize_course(row))
            except Exception as e:
                print(f"Could not load courses CSV: {e}")
                courses = self.DUMMY_COURSES
        else:
            # Use dummy courses if file doesn't exist
            courses = self.DUMMY_COURSES
        
        return courses

    def _normalize_course(self, row: Dict) -> Dict:
        """Normalize CSV rows into a consistent course schema"""
        title = row.get('title') or row.get('course_name') or 'Untitled'
        platform = row.get('platform', 'Unknown')
        url = row.get('url', '')
        price_raw = row.get('price', row.get('cost', 0))
        try:
            price = float(price_raw) if str(price_raw).strip() != '' else 0
        except ValueError:
            price = 0
        duration = row.get('duration') or row.get('duration_hours') or 'N/A'
        level = row.get('level', 'N/A')
        try:
            rating = float(row.get('rating', 0))
        except ValueError:
            rating = 0
        description = row.get('description', 'N/A')
        skills_raw = row.get('skills') or row.get('skill') or ''
        skills = [s.strip().lower() for s in str(skills_raw).replace('|', ';').split(';') if s.strip()]
        if not skills:
            skills = [s.strip().lower() for s in str(skills_raw).split(',') if s.strip()]
        
        return {
            'title': title,
            'course_name': title,
            'platform': platform,
            'url': url,
            'price': price,
            'duration': duration,
            'level': level,
            'rating': rating,
            'description': description,
            'skills': skills,
            'is_free': price == 0,
        }

    def recommend(self, missing_skills: List[Dict], n_per_skill: int = 2) -> List[Dict]:
        """
        Recommend courses for missing skills
        
        Args:
            missing_skills: List of dicts with 'skill' and 'priority' keys
            n_per_skill: Number of recommendations per skill
            
        Returns:
            List of recommended courses with relevance scores
        """
        recommendations = []
        
        for skill_info in missing_skills:
            skill = skill_info.get('skill', '')
            priority = skill_info.get('priority', 'Medium')
            
            # Find matching courses
            matched_courses = self._find_courses(skill, n_per_skill)
            
            for course in matched_courses:
                course['priority'] = priority
                recommendations.append(course)
        
        # Sort by priority and relevance
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        recommendations.sort(
            key=lambda x: (
                priority_order.get(x['priority'], 3),
                x.get('relevance_score', 0)
            ),
            reverse=True
        )
        
        return recommendations

    
    def _find_courses(self, skill: str, n: int = 2) -> List[Dict]:
        """Find top N courses for a skill"""
        if not self.courses:
            return []
        
        # Calculate relevance scores
        skill_lower = skill.lower()
        scored_courses = []
        
        for course in self.courses:
            course_skills = [s.lower() for s in course.get('skills', [])]
            title = str(course.get('title', '')).lower()
            description = str(course.get('description', '')).lower()
            
            if any(skill_lower == s or skill_lower in s for s in course_skills):
                relevance = 1.0
            elif skill_lower in title or skill_lower in description:
                relevance = 0.8
            else:
                from fuzzywuzzy import fuzz
                skills_text = ' '.join(course_skills)
                relevance = fuzz.token_set_ratio(skill_lower, skills_text) / 100.0
            
            if relevance > 0.5:
                course_copy = dict(course)
                course_copy['relevance_score'] = relevance
                scored_courses.append(course_copy)
        
        # Sort by relevance and return top N
        scored_courses.sort(key=lambda x: x['relevance_score'], reverse=True)
        return scored_courses[:n]
    
    def generate_learning_path(self, missing_skills: List[Dict]) -> Dict:
        """Generate a structured learning path"""
        # Get all recommendations
        all_recommendations = self.recommend(missing_skills)
        
        # Group by priority
        by_priority = {'High': [], 'Medium': [], 'Low': []}
        for course in all_recommendations:
            priority = course.get('priority', 'Medium')
            if priority in by_priority:
                by_priority[priority].append(course)
        
        # Estimate total time
        total_hours = sum(
            float(c.get('duration_hours', 0))
            for c in all_recommendations
        )
        
        # Estimate weeks (assuming 15 hours per week study)
        weeks_needed = max(1, int(total_hours / 15))
        
        return {
            'phase_1_high_priority': by_priority['High'][:3],
            'phase_2_medium_priority': by_priority['Medium'][:3],
            'phase_3_low_priority': by_priority['Low'][:2],
            'total_hours': total_hours,
            'estimated_weeks': weeks_needed,
            'all_courses': all_recommendations
        }


# Module-level function for backward compatibility
def recommend_courses(missing_skills: List[Dict]) -> List[Dict]:
    """Recommend courses for missing skills"""
    recommender = Recommender()
    return recommender.recommend(missing_skills)
