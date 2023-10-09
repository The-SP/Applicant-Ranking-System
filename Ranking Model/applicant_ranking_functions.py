import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def calculate_total_score(df_resume_rankings, description_weight, skills_weight, projects_weight, education_weight, experience_weight):
    df_resume_rankings['total_score'] = df_resume_rankings['description_score']*description_weight + df_resume_rankings['skills_score']*skills_weight + df_resume_rankings['projects_score']*projects_weight + df_resume_rankings['education_score']*education_weight + df_resume_rankings['experience_score']*experience_weight

    # Sort the DataFrame based on total_score in descending order
    df_resume_rankings_sorted = df_resume_rankings.sort_values(by='total_score', ascending=False)

    return df_resume_rankings_sorted


def visualize_heatmap(df):
    columns_to_visualize = ['description_score', 'skills_score', 'projects_score', 'education_score', 'experience_score', 'total_score']
    plt.figure(figsize=(10, 6))
    sns.heatmap(df[columns_to_visualize], cmap='YlGnBu', annot=True, fmt=".2f")
    plt.title('Applicant Rankings Score - Heatmap')
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Convert the Matplotlib plot to a Streamlit plot using st.pyplot()
    st.pyplot(plt)