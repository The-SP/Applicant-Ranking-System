def calculate_total_score(df_resume, weights):
    df_resume["total_score"] = (
        df_resume["description_score"] * weights["description"]
        + df_resume["skills_score"] * weights["skills"]
        + df_resume["projects_score"] * weights["projects"]
        + df_resume["education_score"] * weights["education"]
        + df_resume["experience_score"] * weights["experience"]
    )

    # Sort the DataFrame based on total_score in descending order
    df_resume_rankings_sorted = df_resume.sort_values(by="total_score", ascending=False)

    return df_resume_rankings_sorted
