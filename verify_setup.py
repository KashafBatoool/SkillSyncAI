#!/usr/bin/env python
"""
SkillSync Project Verification & Setup Script
Checks all components and helps with initial setup
"""

import os
import sys
from pathlib import Path


def check_project_structure():
    """Verify all project files exist"""
    print("🔍 Verifying Project Structure...")
    print("-" * 60)
    
    required_files = {
        'Core Modules': [
            'modules/__init__.py',
            'modules/resume_parser.py',
            'modules/skill_extractor.py',
            'modules/ats_scorer.py',
            'modules/gap_analyzer.py',
            'modules/recommender.py',
            'modules/career_predictor.py',
            'modules/llm_explainer.py',
        ],
        'Web Application': [
            'app/main.py',
            'app/pages/01_resume_analysis.py',
            'app/pages/02_job_matching.py',
            'app/pages/03_skill_gap.py',
            'app/pages/04_recommendations.py',
            'app/pages/05_career_prediction.py',
        ],
        'Configuration': [
            'pipeline.py',
            'requirements.txt',
            '.env.template',
            '.gitignore',
        ],
        'Database': [
            'database/init_db.py',
            'database/schema.sql',
        ],
        'Streamlit Config': [
            '.streamlit/config.toml',
            '.streamlit/secrets.toml',
        ],
        'Data': [
            'data/raw/courses.csv',
        ]
    }
    
    all_good = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file in files:
            path = Path(file)
            if path.exists():
                size = path.stat().st_size if path.is_file() else 'dir'
                print(f"  ✅ {file} ({size} bytes)" if isinstance(size, int) else f"  ✅ {file}")
            else:
                print(f"  ❌ {file} - MISSING!")
                all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("✅ ALL PROJECT FILES VERIFIED!")
    else:
        print("⚠️ Some files are missing. Please re-run the setup.")
    
    return all_good


def check_virtual_environment():
    """Check if virtual environment exists"""
    print("\n🐍 Checking Python Environment...")
    print("-" * 60)
    
    venv_path = Path('.venv')
    if venv_path.exists():
        print(f"✅ Virtual environment found: {venv_path.absolute()}")
        python_exe = venv_path / 'Scripts' / 'python.exe'
        if python_exe.exists():
            print(f"✅ Python executable: {python_exe}")
            return True
        else:
            print("❌ Python executable not found in venv")
            return False
    else:
        print("❌ Virtual environment not found (.venv/)")
        print("\n💡 To create it, run:")
        print("   python -m venv .venv")
        return False


def check_dependencies():
    """Check if key packages are installed"""
    print("\n📦 Checking Installed Packages...")
    print("-" * 60)
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'sklearn',
        'requests',
        'fuzzywuzzy',
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            all_installed = False
    
    if not all_installed:
        print("\n💡 To install dependencies, run:")
        print("   .\.venv\Scripts\pip.exe install -r requirements.txt")
    
    return all_installed


def main():
    """Run all checks"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "     SkillSync - Project Verification & Setup".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Run checks
    files_ok = check_project_structure()
    venv_ok = check_virtual_environment()
    deps_ok = check_dependencies()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Project Files:        {'✅ OK' if files_ok else '❌ Missing'}")
    print(f"Virtual Environment:  {'✅ OK' if venv_ok else '❌ Missing'}")
    print(f"Dependencies:         {'✅ OK' if deps_ok else '❌ Missing'}")
    
    print("\n" + "=" * 60)
    
    if files_ok and venv_ok and deps_ok:
        print("\n🚀 ALL SYSTEMS GO!")
        print("\nTo start the application, run:")
        print("\n  .\.venv\Scripts\python.exe -m streamlit run app/main.py")
        print("\nThen open: http://localhost:8501")
        return 0
    else:
        print("\n⚠️ SETUP INCOMPLETE")
        print("\nMissing components:")
        if not files_ok:
            print("  • Project files - Re-run the project creation")
        if not venv_ok:
            print("  • Virtual environment - Run: python -m venv .venv")
        if not deps_ok:
            print("  • Dependencies - Run: pip install -r requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
