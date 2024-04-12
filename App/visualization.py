import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def visualize_total_scores(df):
    st.subheader("Resume scores")

    # Bar chart for total scores using seaborn
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x="Filename", y="total_score", data=df)
    for p in ax.patches:
        ax.annotate(
            f"{int(p.get_height()*100)}", (p.get_x() * 1.01, p.get_height() * 1.01)
        )
    plt.xticks(rotation=45)
    plt.title("Total Scores by Resume")
    st.pyplot(plt)


def visualize_feature_weights(weights):
    # Set up the figure and axis
    plt.figure(figsize=(4, 4))
    sns.set_palette("pastel")
    plt.title("Weight distribution for features")
    plt.pie(weights.values(), labels=weights.keys(), autopct="%1.1f%%", startangle=140)
    # Display the pie chart
    st.pyplot(plt)


def visualize_heatmap(df):
    columns_to_visualize = [
        "description_score",
        "skills_score",
        "projects_score",
        "education_score",
        "experience_score",
        "total_score",
    ]

    # Set 'Filename' as the index
    df = df.set_index("Filename")

    # Create a dictionary to map the column names
    column_name_mapping = {
        "description_score": "Description",
        "skills_score": "Skills",
        "projects_score": "Projects",
        "education_score": "Education",
        "experience_score": "Experience",
        "total_score": "Total",
    }

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        df[columns_to_visualize].head(20),
        cmap="YlGnBu",
        annot=True,
        fmt=".2f",
        xticklabels=[column_name_mapping[col] for col in columns_to_visualize],
    )
    plt.title("Applicant Rankings Score - Heatmap")
    plt.tight_layout()
    st.pyplot(plt)
