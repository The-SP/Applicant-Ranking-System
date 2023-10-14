import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_total_scores(df_resume_rankings):
    st.subheader("Resume scores")

    # Bar chart for total scores using seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Filename", y="total_score", data=df_resume_rankings)
    plt.xticks(rotation=45)
    plt.title("Total Scores by Resume")
    st.pyplot(plt)


def visualize_grouped_bar_chart(df_resume_rankings):
    # Grouped bar chart for section scores
    plt.figure(figsize=(12, 6))

    # Select relevant columns for the bar chart
    scores = df_resume_rankings[[
        "description_score",
        "skills_score",
        "projects_score",
        "education_score",
        "experience_score",
        "total_score"
    ]]

    # Transpose the DataFrame for easier plotting
    scores = scores.transpose()

    # Plot the grouped bar chart
    scores.plot(kind='bar')
    plt.xlabel('Sections')
    plt.ylabel('Score')
    plt.title('Scores for Each Section')
    plt.xticks(rotation=45)
    plt.legend(title='Resumes', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Display the plot using st.pyplot()
    st.pyplot(plt)
    

weights = {
    "Description": 0.2,
    "Skills": 0.3,
    "Projects": 0.2,
    "Education": 0.15,
    "Experience": 0.15
}
def visualize_feature_weights():
    # Set up the figure and axis
    plt.figure(figsize=(8, 8))

    sns.set_palette("pastel")
    plt.title('Weight distribution for features')
    plt.pie(weights.values(), labels=weights.keys(), autopct='%1.1f%%', startangle=140)

    # Display the pie chart
    st.pyplot(plt)