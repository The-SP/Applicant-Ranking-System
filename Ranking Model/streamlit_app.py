import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from applicant_ranking_functions import calculate_total_score, visualize_heatmap

def main():
    st.title('Applicant Ranking System')
    
    # Read the resume datasets
    resume_df = pd.read_csv('df_resume_rankings.csv')
    
    # Create UI elements in the sidebar
    st.sidebar.header('Settings')
    description_weight = st.sidebar.slider('Description Weight', 0.0, 1.0, 0.2)
    skills_weight = st.sidebar.slider('Skills Weight', 0.0, 1.0, 0.3)
    projects_weight = st.sidebar.slider('Projects Weight', 0.0, 1.0, 0.2)
    education_weight = st.sidebar.slider('Education Weight', 0.0, 1.0, 0.15)
    experience_weight = st.sidebar.slider('Experience Weight', 0.0, 1.0, 0.15)
    
    if st.sidebar.button('Rank Applicants'):
        # Calculate the total score using the specified weights
        df_resume_rankings = calculate_total_score(resume_df, description_weight, skills_weight, projects_weight, education_weight, experience_weight)
        
        st.subheader('Ranked Applicants')
        st.dataframe(df_resume_rankings)
        st.subheader('Applicant Rankings - Heatmap')

        visualize_heatmap(df_resume_rankings)

if __name__ == '__main__':
    main()
