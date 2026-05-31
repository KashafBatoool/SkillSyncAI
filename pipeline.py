"""
Pipeline module for SkillSync - orchestrates all analyses
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
from datetime import datetime

from modules.resume_parser import ResumeParser
from modules.skill_extractor import SkillExtractor
from modules.ats_scorer import ATSScorer
from modules.gap_analyzer import GapAnalyzer
from modules.recommender import Recommender
from modules.career_predictor import CareerPredictor
from modules.llm_explainer import LLMExplainer


class SkillSyncPipeline:
    """Main orchestrator for SkillSync analyses"""
    
    def __init__(self):
        """Initialize all modules"""
        self.resume_parser = ResumeParser()
        self.skill_extractor = SkillExtractor()
        self.ats_scorer = ATSScorer()
        self.gap_analyzer = GapAnalyzer()
        self.recommender = Recommender()
        self.career_predictor = CareerPredictor()
        self.llm_explainer = LLMExplainer()
        
    def analyze(self, resume_text: str, job_description: str, 
                user_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run complete analysis pipeline
        
        Args:
            resume_text: Extracted resume text
            job_description: Job description to match against
            user_profile: Optional user profile (experience level, goals, etc.)
            
        Returns:
            Dictionary containing all analysis results
        """
        try:
            # Step 1: Parse resume
            parsed_resume = self.resume_parser.parse(resume_text)
            
            # Step 2: Extract skills from resume
            resume_skills = self.skill_extractor.extract(resume_text)
            
            # Step 3: Extract skills from job description
            job_skills = self.skill_extractor.extract(job_description)
            
            # Step 4: Calculate ATS score
            ats_score = self.ats_scorer.score(resume_text, job_description)
            ats_details = self.ats_scorer.get_details()
            
            # Step 5: Analyze skill gaps
            gap_analysis = self.gap_analyzer.analyze(
                resume_skills=resume_skills,
                job_skills=job_skills
            )
            
            # Step 6: Generate recommendations
            # GapAnalyzer returns prioritized missing skills under the 'missing' key
            missing_skills = gap_analysis.get('missing', [])
            # Use Recommender.recommend which accepts a list of skill dicts
            recommendations = self.recommender.recommend(missing_skills, n_per_skill=2)
            
            # Step 7: Predict career matches
            # CareerPredictor.predict expects a list of skills
            career_predictions = self.career_predictor.predict(resume_skills, top_n=5)
            
            # Step 8: Generate explanations (use existing LLMExplainer methods)
            try:
                gap_explanation = self.llm_explainer.explain_skill_gap(gap_analysis)
            except Exception:
                gap_explanation = ''

            # Synthesize explanations for top recommendations
            rec_explanations = []
            for course in recommendations[:5]:
                try:
                    rec_explanations.append(self.llm_explainer.explain_learning_resource(course))
                except Exception:
                    continue

            explanations = {
                'gap_explanation': gap_explanation,
                'recommendations_explanation': '\n\n'.join(rec_explanations)
            }
            
            # Compile complete results
            results = {
                'timestamp': datetime.now().isoformat(),
                'parsed_resume': parsed_resume,
                'resume_skills': resume_skills,
                'job_skills': job_skills,
                'ats_score': ats_score,
                'ats_details': ats_details,
                'gap_analysis': gap_analysis,
                'recommendations': recommendations,
                'career_predictions': career_predictions,
                'explanations': explanations,
                'status': 'success'
            }
            
            return results
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """
        Generate a text report from analysis results
        
        Args:
            analysis_results: Results from analyze() method
            
        Returns:
            Formatted report string
        """
        if analysis_results.get('status') == 'error':
            return f"Error in analysis: {analysis_results.get('error')}"
        
        report = []
        report.append("=" * 80)
        report.append("SKILLSYNC ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: {analysis_results['timestamp']}")
        
        # Resume Info
        resume = analysis_results['parsed_resume']
        report.append("\n--- RESUME INFORMATION ---")
        report.append(f"Name: {resume.get('name', 'N/A')}")
        report.append(f"Title: {resume.get('title', 'N/A')}")
        report.append(f"Years of Experience: {resume.get('years_experience', 'N/A')}")
        report.append(f"Experience Level: {resume.get('experience_level', 'N/A')}")
        
        # Skills Summary
        report.append("\n--- SKILLS SUMMARY ---")
        report.append(f"Resume Skills: {len(analysis_results['resume_skills'])}")
        report.append(f"Job Requirements: {len(analysis_results['job_skills'])}")
        
        # ATS Score
        report.append("\n--- ATS SCORE ---")
        report.append(f"Score: {analysis_results['ats_score']:.1f}%")
        report.append(f"Details: {analysis_results['ats_details']}")
        
        # Gap Analysis
        gap = analysis_results['gap_analysis']
        report.append("\n--- SKILL GAP ANALYSIS ---")
        report.append(f"Matched Skills: {len(gap.get('matched_skills', []))}")
        report.append(f"Missing Skills: {len(gap.get('missing_skills', []))}")
        report.append(f"Excess Skills: {len(gap.get('excess_skills', []))}")
        
        if gap.get('missing_skills'):
            report.append(f"  Missing: {', '.join(gap['missing_skills'][:5])}")
        
        # Recommendations
        report.append("\n--- TOP RECOMMENDATIONS ---")
        for i, rec in enumerate(analysis_results['recommendations'][:5], 1):
            report.append(f"{i}. {rec.get('title', 'Unknown')}")
            report.append(f"   Platform: {rec.get('platform', 'N/A')}")
            report.append(f"   Duration: {rec.get('duration', 'N/A')}")
        
        # Career Predictions
        report.append("\n--- CAREER MATCHES ---")
        for i, career in enumerate(analysis_results['career_predictions'][:3], 1):
            report.append(f"{i}. {career.get('title', 'Unknown')}")
            report.append(f"   Confidence: {career.get('confidence', 0):.1f}%")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)
    
    def save_results(self, analysis_results: Dict[str, Any], 
                     filepath: Optional[str] = None) -> str:
        """
        Save analysis results to JSON file
        
        Args:
            analysis_results: Results from analyze() method
            filepath: Optional path to save results (defaults to timestamped file)
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"results/analysis_{timestamp}.json"
        
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        return filepath
