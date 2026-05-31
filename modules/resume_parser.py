"""
Resume Parser Module - Extracts text and sections from resume files
Supports PDF, DOCX, and TXT formats
"""

import os
import re
import PyPDF2
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import docx


class ResumeParser:
    """Parse and extract information from resume documents"""
    
    # Resume section headers to look for
    SECTION_KEYWORDS = {
        'SUMMARY': ['professional summary', 'summary', 'objective', 'profile'],
        'EXPERIENCE': ['work experience', 'experience', 'employment', 'professional experience', 'career history'],
        'EDUCATION': ['education', 'academic', 'qualification', 'degree', 'university'],
        'SKILLS': ['skills', 'technical skills', 'competencies', 'core competencies'],
        'PROJECTS': ['projects', 'portfolio', 'sample work', 'github'],
        'CERTIFICATIONS': ['certifications', 'certificates', 'credentials', 'licenses'],
    }
    
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_PATTERN = r'(?:\+1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
    LINKEDIN_PATTERN = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
    
    def __init__(self, debug: bool = False):
        """Initialize the parser"""
        self.debug = debug
    
    def parse(self, resume_text: str) -> Dict:
        """
        Parse resume text and extract structured information
        
        Args:
            resume_text: Raw resume text content
            
        Returns:
            Dict with keys:
            - raw_text: Full text content
            - sections: Dict of section_name -> section_text
            - contact_info: Dict with email, phone, linkedin
            - name: Extracted name
            - title: Extracted title
            - years_experience: Estimated years of experience
        """
        # Clean text
        raw_text = self._clean_text(resume_text)
        
        # Extract structured sections
        sections = self._split_sections(raw_text)
        
        # Extract contact information
        contact_info = self._extract_contact_info(raw_text)
        
        # Extract name and title (simple heuristics)
        name = self._extract_name(raw_text)
        title = self._extract_title(raw_text)
        years_experience = self._estimate_experience(raw_text)
        
        return {
            'raw_text': raw_text,
            'sections': sections,
            'contact_info': contact_info,
            'name': name,
            'title': title,
            'years_experience': years_experience
        }
    
    def parse_file(self, file_path: str) -> Dict:
        """
        Parse a resume file and extract structured information
        
        Args:
            file_path: Path to resume file (PDF, DOCX, or TXT)
            
        Returns:
            Dict with keys:
            - raw_text: Full text content
            - sections: Dict of section_name -> section_text
            - contact_info: Dict with email, phone, linkedin
            - file_type: pdf, docx, or txt
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        file_ext = file_path.suffix.lower()
        
        # Extract text based on file type
        if file_ext == '.pdf':
            raw_text = self._extract_pdf(str(file_path))
        elif file_ext == '.docx':
            raw_text = self._extract_docx(str(file_path))
        elif file_ext == '.txt':
            raw_text = self._extract_txt(str(file_path))
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        # Clean text
        raw_text = self._clean_text(raw_text)
        
        # Extract structured sections
        sections = self._split_sections(raw_text)
        
        # Extract contact information
        contact_info = self._extract_contact_info(raw_text)
        
        return {
            'raw_text': raw_text,
            'sections': sections,
            'contact_info': contact_info,
            'file_type': file_ext.strip('.')
        }
    
    def _extract_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    def _extract_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting DOCX: {str(e)}")
    
    def _extract_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error extracting TXT: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep periods, commas, parentheses
        text = re.sub(r'[^\w\s.,()@-]', '', text)
        return text.strip()
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract email, phone, linkedin from resume text"""
        contact = {
            'email': None,
            'phone': None,
            'linkedin': None
        }
        
        # Extract email
        email_match = re.search(self.EMAIL_PATTERN, text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Extract phone
        phone_match = re.search(self.PHONE_PATTERN, text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        # Extract LinkedIn
        linkedin_match = re.search(self.LINKEDIN_PATTERN, text)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group(0)
        
        return contact
    
    def _split_sections(self, text: str) -> Dict[str, str]:
        """Split resume into structured sections"""
        sections = {}
        text_upper = text.upper()
        
        for section_name, keywords in self.SECTION_KEYWORDS.items():
            for keyword in keywords:
                keyword_upper = keyword.upper()
                if keyword_upper in text_upper:
                    start_idx = text_upper.find(keyword_upper)
                    # Find next section start
                    end_idx = len(text)
                    for other_section, other_keywords in self.SECTION_KEYWORDS.items():
                        if other_section != section_name:
                            for other_keyword in other_keywords:
                                other_idx = text_upper.find(other_keyword.upper(), start_idx + len(keyword_upper))
                                if other_idx > start_idx and other_idx < end_idx:
                                    end_idx = other_idx
                    
                    sections[section_name] = text[start_idx:end_idx].strip()
                    break
        
        # Add full text if no sections found
        if not sections:
            sections['FULL_TEXT'] = text
        
        return sections
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume text (simple heuristic)"""
        lines = text.split('\n')[:5]  # Check first 5 lines
        for line in lines:
            line = line.strip()
            if len(line.split()) >= 2 and len(line) < 50:  # Likely a name
                return line
        return "Unknown"
    
    def _extract_title(self, text: str) -> str:
        """Extract job title from resume text"""
        # Look for common title patterns
        title_patterns = [
            r'(?i)(software engineer|developer|analyst|manager|consultant|architect)',
            r'(?i)(data scientist|machine learning|ai engineer)',
            r'(?i)(full.?stack|front.?end|back.?end)',
        ]
        for pattern in title_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0).title()
        return "Professional"
    
    def _estimate_experience(self, text: str) -> int:
        """Estimate years of experience from resume text"""
        # Simple keyword-based estimation
        exp_keywords = ['year', 'years', 'experience']
        text_lower = text.lower()
        years = 0
        
        # Look for explicit year mentions
        year_matches = re.findall(r'(\d+)\s*(?:year|yr)', text_lower)
        if year_matches:
            years = max([int(y) for y in year_matches])
        
        # Fallback based on keywords
        if years == 0:
            if 'senior' in text_lower or 'lead' in text_lower:
                years = 5
            elif 'junior' in text_lower or 'entry' in text_lower:
                years = 1
            else:
                years = 3  # Default
        
        return years


# For backward compatibility - create module-level function
def parse_resume(file_path: str) -> Dict:
    """Module-level function to parse a resume"""
    parser = ResumeParser()
    return parser.parse_file(file_path)
