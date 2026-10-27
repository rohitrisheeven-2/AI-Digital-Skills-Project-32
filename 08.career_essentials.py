"""
08. Career Essentials & Competency Radar Visualizer
Maps core career readiness dimensions against target role benchmarks and outputs
a high-resolution radar chart (08.career_skills_radar.png).
"""

import numpy as np
import matplotlib.pyplot as plt

def generate_skills_radar(output_path: str = "08.career_skills_radar.png"):
    categories = [
        "AI Fluency & Prompting",
        "Software Engineering & Git",
        "Data Analytics & BI",
        "Cybersecurity Hygiene",
        "Problem Solving & DSA",
        "Communication & Branding"
    ]
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    current_skills = [88, 85, 82, 78, 86, 84]
    target_benchmark = [90, 90, 85, 85, 90, 85]

    current_skills += current_skills[:1]
    target_benchmark += target_benchmark[:1]

    fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True), dpi=150)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories, fontsize=10, fontweight="bold")
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="#475569", size=8)
    plt.ylim(0, 105)

    ax.plot(angles, current_skills, linewidth=2.5, linestyle="solid", label="Portfolio Demonstrated Competency", color="#2563eb")
    ax.fill(angles, current_skills, color="#3b82f6", alpha=0.28)

    ax.plot(angles, target_benchmark, linewidth=2.0, linestyle="dashed", label="Industry Target Benchmark", color="#0f172a")

    plt.title("Career Essentials: Multi-Domain Competency Radar", size=14, fontweight="bold", y=1.08)
    plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    generate_skills_radar()
    print("Generated 08.career_skills_radar.png successfully.")
