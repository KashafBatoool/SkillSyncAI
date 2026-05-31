#!/usr/bin/env python
"""
Simple Streamlit launcher for SkillSync
"""
import subprocess
import sys
import os

# Ensure we're using the activated environment
os.chdir(r'c:\Users\HP\Documents\Skill gap analyser')

# Try to import streamlit to make sure it's available
try:
    import streamlit
    print(f"✅ Streamlit {streamlit.__version__} is installed")
except ImportError:
    print("❌ Streamlit not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "pandas", "numpy"], 
                   capture_output=True)
    import streamlit
    print(f"✅ Streamlit {streamlit.__version__} installed successfully")

print("🚀 Launching SkillSync...")
print("Opening http://localhost:8501")

# Launch streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"])
