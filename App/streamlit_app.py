import streamlit as st

from resume_parse import parse_resume_files
from applicant_ranking import ranking_algorithm
from visualization import (
    visualize_total_scores,
    visualize_feature_weights,
    visualize_heatmap,
)


def main():
    # Set the page title
    st.set_page_config(page_title="Resume Ranker")
    st.title("Applicant Ranking System")

    # Set default values
    default_data = {
        "title": "Full Stack Web Developer",
        "description": "We are seeking a talented and motivated Full Stack Developer to join our dynamic team at XYZ Tech Solutions. As a key member of our development team, you will be responsible for designing, developing, and maintaining scalable web applications, collaborating closely with cross-functional teams to meet project requirements. The ideal candidate will have a strong foundation in both front-end and back-end technologies, proficiency in frameworks like React or Angular, and experience with database management systems. You should be adept at writing clean, efficient code, conducting thorough testing, and staying updated on industry trends. If you are a proactive problem solver with excellent communication skills and a passion for innovation, we invite you to apply and contribute to the exciting projects shaping the future of our company in the technology sector. Join us in a collaborative and inclusive work environment where your skills will thrive, and together, we'll make a meaningful impact. Apply by [closing date] with your resume, cover letter, and any relevant portfolio to careers@xyztechsolutions.com. XYZ Tech Solutions is proud to be an equal opportunity employer, offering competitive benefits and a platform for professional growth.",
        "skills": "React.js, Node.js, HTML, CSS, JavaScript, Python, SQL, PostgreSQL",
        "education": "Bachelor in Computer Engineering",
        "experience": "3 years",
    }

    # Job Description Inputs
    st.subheader("Job Description")
    title = st.text_input("Title", default_data["title"])
    description = st.text_area("Description", default_data["description"], height=200)
    skills = st.text_input("Skills", default_data["skills"])
    education = st.text_input("Education", default_data["education"])
    experience = st.text_input("Experience", default_data["experience"])

    # Add input fields for weights on the same line
    st.subheader("Weights")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        weight_description = round(
            st.number_input(
                "Description",
                min_value=0.0,
                max_value=1.0,
                value=0.15,
                step=0.05,
            ),
            2,
        )

    with col2:
        weight_education = round(
            st.number_input(
                "Education",
                min_value=0.0,
                max_value=1.0,
                value=0.2,
                step=0.05,
            ),
            2,
        )

    with col3:
        weight_experience = round(
            st.number_input(
                "Experience",
                min_value=0.0,
                max_value=1.0,
                value=0.35,
                step=0.05,
            ),
            2,
        )

    with col4:
        weight_skills = round(
            st.number_input(
                "Skills",
                min_value=0.0,
                max_value=1.0,
                value=0.2,
                step=0.05,
            ),
            2,
        )

    with col5:
        weight_projects = round(
            st.number_input(
                "Projects",
                min_value=0.0,
                max_value=1.0,
                value=0.10,
                step=0.05,
                #
            ),
            2,
        )

    # Ensure that the sum of weights is 1
    total_weight = round(
        (
            weight_description
            + weight_education
            + weight_experience
            + weight_skills
            + weight_projects
        ),
        2,
    )

    if total_weight != 1:
        st.warning(
            f"The total weight is {total_weight}. Please adjust the weights to ensure they add up to 1."
        )

    # Create a dictionary with the input data
    weights = {
        "description": weight_description,
        "education": weight_education,
        "experience": weight_experience,
        "skills": weight_skills,
        "projects": weight_projects,
    }

    # Create a dictionary with the input data
    data = {
        "title": title,
        "description": description,
        "skills": skills,
        "education": education,
        "experience": experience,
    }

    # Update 'target_job' based on input provided
    target_job = data if all(data.values()) else {}

    # Resume Upload
    # Check if the target job is not empty dictionary
    if target_job and total_weight == 1:
        if st.checkbox("Visualize feature weights"):
            visualize_feature_weights(weights)

        # Convert the dictionary to a Series
        st.subheader("Upload Resumes")
        resumes = st.file_uploader(
            "Upload Applicant's Resumes", type=["pdf"], accept_multiple_files=True
        )

        if resumes:
            if st.button("Parse Resume"):
                info_message1 = st.info(
                    "Processing uploaded resumes to extract relevant information..."
                )
                parse_resume_files(resumes)
                info_message2 = st.info(
                    "Evaluating candidates..."
                )

                df_resume_rankings = ranking_algorithm(target_job, weights)

                info_message1.empty()  # Remove the info message
                info_message2.empty()  # Remove the info message

                st.subheader("Final Resume Rankings")
                st.write(
                    df_resume_rankings[
                        [
                            "Filename",
                            "total_score",
                            "description_score",
                            "education_score",
                            "experience_score",
                            "skills_score",
                            "projects_score",
                        ]
                    ]
                )

                visualize_total_scores(df_resume_rankings)
                visualize_heatmap(df_resume_rankings)


if __name__ == "__main__":
    main()
