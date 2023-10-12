import matplotlib.pyplot as plt
import seaborn as sns


def calculate_total_score(df_resume):
    description_weight = 0.2
    skills_weight = 0.3
    projects_weight = 0.2
    education_weight = 0.15
    experience_weight = 0.15

    df_resume["total_score"] = (
        df_resume["description_score"] * description_weight
        + df_resume["skills_score"] * skills_weight
        + df_resume["projects_score"] * projects_weight
        + df_resume["education_score"] * education_weight
        + df_resume["experience_score"] * experience_weight
    )

    # Sort the DataFrame based on total_score in descending order
    df_resume_rankings_sorted = df_resume.sort_values(by="total_score", ascending=False)

    return df_resume_rankings_sorted


def visualize_heatmap(df):
    columns_to_visualize = [
        "description_score",
        "skills_score",
        "projects_score",
        "education_score",
        "experience_score",
        "total_score",
    ]
    plt.figure(figsize=(10, 6))
    sns.heatmap(df[columns_to_visualize], cmap="YlGnBu", annot=True, fmt=".2f")
    plt.title("Applicant Rankings Score - Heatmap")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
