# SkillSync AI Resume Analyzer - Academic Project Report

## Abstract
This report presents the design, implementation, and verification of SkillSync, an AI-assisted resume analysis system that performs resume parsing, skill extraction, job matching, gap analysis, course recommendation, and career prediction. The system integrates a modular Python backend with a Streamlit-based interface and a lightweight SQLite store. Verification confirms end-to-end functionality across all user-facing pages and validates skill extraction performance on a controlled sample. The report emphasizes the system architecture, algorithmic methodology, and empirical checkpoints that support readiness for local deployment.

## 1. Introduction
SkillSync addresses the problem of aligning candidate skills with job requirements by automating resume analysis and generating actionable learning guidance. The project emphasizes local execution, privacy, and an explainable pipeline architecture. The design objective is to provide a reproducible, end-to-end workflow that transforms unstructured resume and job description text into structured insights that are interpretable and actionable.

## 2. System Overview
The system is organized into a UI layer, orchestration pipeline, and domain modules. The user interacts through a five-page Streamlit interface, which invokes a pipeline that coordinates resume parsing, skill extraction, ATS scoring, gap analysis, recommendations, and career prediction. The modular design isolates each analytic stage, enabling targeted testing and improvement without cross-module regressions.

## 3. Methodology
- Resume parsing uses format-specific extractors for PDF, DOCX, and TXT files with section-aware cleanup.
- Skill extraction combines direct, fuzzy, and semantic matching with confidence scoring and de-duplication.
- ATS scoring applies a weighted blend of semantic similarity, TF-IDF, and keyword matching.
- Gap analysis compares extracted resume skills to job requirements and assigns priorities with learning time estimates.
- Recommendations match missing skills to a curated course dataset across multiple platforms and cost tiers.
- Career prediction matches skills against predefined role profiles with confidence scoring and development timelines.

## 4. Implementation Summary
### 4.1 Core Modules
- resume_parser: Structured extraction of resume text and metadata.
- skill_extractor: Multi-method skill identification and scoring.
- ats_scorer: Composite ATS compatibility scoring.
- gap_analyzer: Skill gap categorization and learning time estimates.
- recommender: Course matching and filtering.
- career_predictor: Role matching with confidence scores.
- llm_explainer: Natural language explanations of analysis outputs.

### 4.2 User Interface
Five analysis pages and a dashboard expose the pipeline outputs to end users. The interface supports resume uploads, job description input, and interactive exploration of results. State management ensures consistent navigation across multi-step analyses.

## 5. Verification and Quality Assurance
Testing confirmed end-to-end operation across all pages. A reported skill extraction failure was traced to Streamlit module caching and resolved via cache invalidation and restart. Sample resume testing extracted 74 skills from a controlled resume with explicit keywords. Additional fixes improved gap display sorting and key mapping consistency.

### 5.1 Evaluation Notes
- The evaluation used a controlled resume with explicit skill tokens to validate extraction precision.
- ATS scoring results were validated for consistency across repeated runs.
- Gap analysis outputs were checked for correct separation of matched, missing, and excess skills.

## 6. Results and Metrics
Table 1 summarizes key system metrics based on repository documentation.

**Table 1. System metrics summary**

| Metric | Value |
| --- | --- |
| Total files created | 48 |
| Total code lines | 9,000+ |
| Core modules | 7 |
| UI pages | 5 |
| Career profiles | 8 |
| Skills in master database | 154+ |
| Courses in dataset | 25+ |
| Skills extracted in verification sample | 74 |

Figure 1 shows a distribution of primary system artifacts. Figure 2 summarizes verification outcomes. Figure 3 highlights functional coverage by feature area.

## 7. Visuals
- Figure 1. System artifact counts by category.
- Figure 2. Verification outcome summary.
- Figure 3. Feature coverage by analysis stage.

## 8. Limitations
- Streamlit caching can retain stale module versions after updates.
- Accuracy depends on the quality and specificity of job descriptions and resumes.
- Course dataset requires periodic updates to remain current.
- The current evaluation is based on a controlled sample rather than a large, diverse dataset.

## 9. Future Work
- Expand the skills and course datasets.
- Add analytics and export features.
- Integrate optional semantic similarity enhancements for ATS scoring.
- Conduct a larger-scale evaluation with annotated datasets to quantify precision and recall.

## 10. Conclusion
SkillSync delivers a complete, modular resume analysis pipeline with verified end-to-end functionality. The system is production-ready for local deployment and provides actionable guidance for skill development and career planning.

## Appendix A: Data Sources
Metrics and verification outcomes are derived from the project delivery, verification, and improvements documentation included in the repository.
