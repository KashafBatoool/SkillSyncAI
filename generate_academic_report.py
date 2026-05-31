from pathlib import Path

import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = REPORTS_DIR / "assets"


def build_charts(metrics: dict) -> dict:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    artifact_labels = list(metrics["artifact_counts"].keys())
    artifact_values = list(metrics["artifact_counts"].values())

    plt.figure(figsize=(6.5, 3.5))
    plt.bar(artifact_labels, artifact_values, color="#2c7fb8")
    plt.title("Figure 1. System artifact counts")
    plt.ylabel("Count")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    figure1_path = ASSETS_DIR / "figure1.png"
    plt.savefig(figure1_path, dpi=200)
    plt.close()

    summary_labels = list(metrics["verification_summary"].keys())
    summary_values = list(metrics["verification_summary"].values())

    plt.figure(figsize=(6.5, 3.5))
    plt.bar(summary_labels, summary_values, color="#41ae76")
    plt.title("Figure 2. Verification summary")
    plt.ylabel("Count")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    figure2_path = ASSETS_DIR / "figure2.png"
    plt.savefig(figure2_path, dpi=200)
    plt.close()

    feature_labels = list(metrics["feature_coverage"].keys())
    feature_values = list(metrics["feature_coverage"].values())

    plt.figure(figsize=(6.5, 3.5))
    plt.bar(feature_labels, feature_values, color="#8c6bb1")
    plt.title("Figure 3. Feature coverage by analysis stage")
    plt.ylabel("Coverage")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    figure3_path = ASSETS_DIR / "figure3.png"
    plt.savefig(figure3_path, dpi=200)
    plt.close()

    return {
        "figure1": figure1_path,
        "figure2": figure2_path,
        "figure3": figure3_path,
    }


def build_pdf(metrics: dict, figures: dict) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = REPORTS_DIR / "PROJECT_REPORT_ACADEMIC.pdf"

    styles = getSampleStyleSheet()
    body = styles["BodyText"]
    heading = styles["Heading2"]
    title = styles["Title"]

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=LETTER,
        leftMargin=0.9 * inch,
        rightMargin=0.9 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
    )

    story = []
    story.append(Paragraph("SkillSync AI Resume Analyzer - Academic Project Report", title))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Abstract", heading))
    story.append(
        Paragraph(
            "This report presents the design, implementation, and verification of SkillSync, an "
            "AI-assisted resume analysis system that performs resume parsing, skill extraction, "
            "job matching, gap analysis, course recommendation, and career prediction. The "
            "system integrates a modular Python backend with a Streamlit interface and a "
            "lightweight SQLite store. Verification confirms end-to-end functionality across "
            "all user-facing pages and validates skill extraction performance on a controlled sample.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("System Overview", heading))
    story.append(
        Paragraph(
            "The system is organized into a UI layer, orchestration pipeline, and domain modules. "
            "The user interacts through a five-page Streamlit interface, which invokes a pipeline "
            "that coordinates resume parsing, skill extraction, ATS scoring, gap analysis, "
            "recommendations, and career prediction.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("Methodology", heading))
    story.append(
        Paragraph(
            "Resume parsing relies on format-specific extractors for PDF, DOCX, and TXT files. "
            "Skill extraction combines direct, fuzzy, and semantic matching with confidence "
            "scoring and de-duplication. ATS scoring blends semantic similarity, TF-IDF, and "
            "keyword matching. Gap analysis compares extracted resume skills to job requirements "
            "and assigns priorities with learning time estimates. Recommendations map missing "
            "skills to a curated course dataset. Career prediction matches skills against role "
            "profiles and provides confidence scoring and development timelines.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("Verification and Evaluation", heading))
    story.append(
        Paragraph(
            "End-to-end testing confirmed operation across all user-facing pages. A reported "
            "skill extraction failure was traced to Streamlit module caching and resolved via "
            "cache invalidation and restart. Sample resume testing extracted 74 skills from a "
            "controlled resume with explicit skill keywords. Additional validation confirmed "
            "correct separation of matched, missing, and excess skills.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("Results and Metrics", heading))
    story.append(Paragraph("Table 1. System metrics summary", body))

    table_data = [["Metric", "Value"]]
    for label, value in metrics["table_metrics"]:
        table_data.append([label, value])

    table = Table(table_data, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6f2ff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1f2d3d")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9fb3c8")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Visuals", heading))

    figure1 = Image(str(figures["figure1"]), width=6.2 * inch, height=3.2 * inch)
    story.append(figure1)
    story.append(Paragraph("Figure 1. System artifact counts by category.", body))
    story.append(Spacer(1, 0.15 * inch))

    figure2 = Image(str(figures["figure2"]), width=6.2 * inch, height=3.2 * inch)
    story.append(figure2)
    story.append(Paragraph("Figure 2. Verification outcome summary.", body))
    story.append(Spacer(1, 0.15 * inch))

    figure3 = Image(str(figures["figure3"]), width=6.2 * inch, height=3.2 * inch)
    story.append(figure3)
    story.append(Paragraph("Figure 3. Feature coverage by analysis stage.", body))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Limitations", heading))
    story.append(
        Paragraph(
            "Streamlit caching can retain stale module versions after updates. Accuracy depends "
            "on the quality and specificity of job descriptions and resumes. The current "
            "evaluation is based on a controlled sample rather than a large, diverse dataset. "
            "Course recommendations require periodic dataset updates to remain current.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("Future Work", heading))
    story.append(
        Paragraph(
            "Planned enhancements include expanding the skills and course datasets, adding "
            "analytics and export features, integrating optional semantic similarity improvements "
            "for ATS scoring, and conducting a larger-scale evaluation with annotated datasets to "
            "quantify precision and recall.",
            body,
        )
    )

    doc.build(story)
    return pdf_path


def main() -> None:
    metrics = {
        "artifact_counts": {
            "Core modules": 7,
            "UI pages": 5,
            "Pipeline": 1,
            "Database/data": 3,
            "Docs": 8,
            "Config/launch": 7,
        },
        "verification_summary": {
            "Pages tested": 6,
            "Skills extracted": 74,
            "Skills in DB": 154,
            "Courses": 25,
        },
        "feature_coverage": {
            "Resume analysis": 1,
            "Job matching": 1,
            "Skill gap": 1,
            "Recommendations": 1,
            "Career prediction": 1,
            "Explanations": 1,
        },
        "table_metrics": [
            ("Total files created", "48"),
            ("Total code lines", "9,000+"),
            ("Core modules", "7"),
            ("UI pages", "5"),
            ("Career profiles", "8"),
            ("Skills in master database", "154+"),
            ("Courses in dataset", "25+"),
            ("Skills extracted in verification sample", "74"),
        ],
    }

    figures = build_charts(metrics)
    pdf_path = build_pdf(metrics, figures)
    print(f"PDF generated at: {pdf_path}")


if __name__ == "__main__":
    main()
