import pandas as pd

from description_score import get_description_score
from skill_score import get_skills_score, get_projects_score
from education_score import get_education_score
from experience_score import get_experience_score
from total_score import calculate_total_score, visualize_heatmap


def ranking_algorithm(target_job):
    # df_jobs = pd.read_csv("jobs.csv")
    # target_job = df_jobs.loc[2]

    # print("RESUME PARSING...")
    # parse_resume_files()

    df_resume = pd.read_csv("resume_sections.csv")
    df_resume.fillna("", inplace=True)

    print()
    print("Calculating description score...")
    get_description_score(df_resume, target_job)

    print("Calculating skills score...")
    get_skills_score(df_resume, target_job)

    print("Calculating projects score...")
    get_projects_score(df_resume, target_job)

    print("Calculating education score...")
    get_education_score(df_resume, target_job)

    print("Calculating experience score...")
    get_experience_score(df_resume, target_job)

    print("Calculating Total score...")
    df_resume_rankings_sorted = calculate_total_score(df_resume)

    print("\n Final Results...")
    # print(df_resume.columns)
    print(
        df_resume[
            [
                "Filename",
                # "clean_resume_text",
                "description_score",
                # "SKILLS",
                # "skills_vector",
                "skills_score",
                # "PROJECTS",
                # "projects_vector",
                "projects_score",
                # "EDUCATION",
                # "education_degree",
                # "education_major",
                "education_score",
                # "EXPERIENCE",
                # "experience_dates",
                "experience_score",
                "total_score",
            ]
        ]
    )
    return df_resume_rankings_sorted
    # visualize_heatmap(df_resume)
