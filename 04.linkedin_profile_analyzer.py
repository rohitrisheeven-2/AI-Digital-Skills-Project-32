"""
04. LinkedIn Profile Analyzer & Improvement Visualizer
Evaluates professional profile sections (Headline, About, Experience, Skills, Featured)
and generates a visual comparison chart of before vs. after optimization.
"""

import matplotlib.pyplot as plt
import numpy as np

def score_profile(profile_data: dict) -> dict:
    scores = {}
    # Headline score
    hl_len = len(profile_data.get("headline", ""))
    scores["Headline"] = min(100, int((hl_len / 120) * 70) + (30 if "|" in profile_data.get("headline", "") else 10))
    # Summary score
    summary_words = len(profile_data.get("about", "").split())
    scores["Summary"] = min(100, int((summary_words / 150) * 80) + 20)
    # Experience impact (quantified metrics)
    exp_bullets = profile_data.get("experience_bullets", [])
    quantified = sum(1 for b in exp_bullets if any(c.isdigit() for c in b))
    scores["Experience"] = min(100, int((quantified / max(1, len(exp_bullets))) * 100))
    # Skills & Endorsements
    skills_count = len(profile_data.get("skills", []))
    scores["Skills"] = min(100, skills_count * 8)
    # Projects & Featured
    projects_count = len(profile_data.get("projects", []))
    scores["Projects"] = min(100, projects_count * 25)
    return scores

def generate_improvement_chart(before_scores: dict, after_scores: dict, output_path: str = "04.profile_improvement.png"):
    categories = list(before_scores.keys())
    before_vals = [before_scores[k] for k in categories]
    after_vals = [after_scores[k] for k in categories]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
    rects1 = ax.bar(x - width/2, before_vals, width, label="Before Optimization", color="#94a3b8", edgecolor="#475569")
    rects2 = ax.bar(x + width/2, after_vals, width, label="After Optimization", color="#2563eb", edgecolor="#1e40af")

    ax.set_ylabel("Optimization Score (0 - 100)", fontsize=11, fontweight="bold")
    ax.set_title("LinkedIn Profile Audit: Before vs. After AI Optimization", fontsize=13, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10, fontweight="bold")
    ax.set_ylim(0, 115)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="#f8fafc")

    for rect in rects1 + rects2:
        h = rect.get_height()
        ax.annotate(f"{h}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    before_profile = {
        "headline": "Software Engineer",
        "about": "I am a developer interested in AI and Python programming.",
        "experience_bullets": ["Built backend APIs", "Worked on data pipelines", "Reduced query time by 20%"],
        "skills": ["Python", "SQL", "Git", "Docker", "Linux"],
        "projects": ["Portfolio Website"]
    }
    after_profile = {
        "headline": "AI & Machine Learning Engineer | Building Scalable RAG Systems, Python & Cloud Microservices",
        "about": "Results-driven AI Engineer with experience designing end-to-end machine learning pipelines, automated data workflows, and low-latency APIs. Passionate about agentic workflows, model optimization, and scalable cloud architecture. Proven track record of delivering production solutions that improve operational efficiency.",
        "experience_bullets": [
            "Engineered automated ETL pipeline processing 500k+ daily records, cutting latency by 42%",
            "Deployed RAG microservice achieving 91% retrieval accuracy across 10,000+ internal docs",
            "Optimized SQL queries and caching layers, reducing cloud compute costs by 28%"
        ],
        "skills": ["Python", "PyTorch", "Machine Learning", "SQL", "Docker", "Git", "FastAPI", "RAG", "LangChain", "Data Visualization", "Cloud Computing", "CI/CD"],
        "projects": ["AI Document Assistant", "Sales Analytics Dashboard", "Mini-Git VCS", "Automated Security Scanner"]
    }

    b_scores = score_profile(before_profile)
    a_scores = score_profile(after_profile)
    print("Before Scores:", b_scores)
    print("After Scores:", a_scores)
    generate_improvement_chart(b_scores, a_scores)
    print("Saved chart to 04.profile_improvement.png")
