# Streamlit Cloud Deploy (SkillSync)

## Required files (repo root)
- requirements.txt
- runtime.txt
- .python-version
- .streamlit/config.toml

## Steps
1. Push all files to GitHub.
2. Streamlit Cloud -> New app.
3. Select repo and branch.
4. Main file path: app/main.py
5. Click Deploy.

## Notes
- If build uses Python 3.14, redeploy after confirming runtime.txt and .python-version are in repo root.
- If build fails, open Manage App -> Logs and check the first error line.
