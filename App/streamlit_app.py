import streamlit as st
import pandas as pd

from resume_parse import parse_resume_files
from applicant_ranking import ranking_algorithm


def main():
    st.title("Applicant Ranking System")

    # Job Description Inputs
    st.subheader("Job Description")
    title = st.text_input("Title")
    description = st.text_input("Description")
    skills = st.text_input("Skills")
    education = st.text_input("Education")
    experience = st.text_input("Experience")

    # Create a dictionary with the input data
    data = {
        "title": title,
        "description": description,
        "skills": skills,
        "education": education,
        "experience": experience,
    }

    # Check if 'target_job' already exists in the session state
    if "target_job" not in st.session_state:
        # If not, initialize it as an empty dictionary
        st.session_state["target_job"] = {}

    if title and description and skills and education and experience:
        # Update 'target_job' in the session state
        st.session_state["target_job"].update(data)

    if st.button("Autofill"):
        st.session_state["target_job"]["title"] = "Software Developer"
        st.session_state["target_job"]["description"] = "this is developer job"
        st.session_state["target_job"][
            "skills"
        ] = "Python, Django, Django rest, React, JavaScript"
        st.session_state["target_job"]["education"] = "Bachelor in Computer Engineering"
        st.session_state["target_job"]["experience"] = "2 years"

    # Resume Upload
    # Convert the dictionary to a Series
    target_job = pd.Series(st.session_state["target_job"])
    if not target_job.isnull().any():
        st.subheader("Upload Resumes")
        resumes = st.file_uploader(
            "Upload Applicant's Resumes", type=["pdf"], accept_multiple_files=True
        )

        if st.button("Display Filenames"):
            if resumes is not None:
                # Join all filenames into a single string
                filenames = " | ".join([resume.name for resume in resumes])
                st.write(filenames)

        if st.button("Parse Resume"):
            st.write(target_job)
            if resumes is not None:
                st.write("Parsing Resume Files...")
                parse_resume_files(resumes)
                st.write("Evaluating Resumes...")
                df_resume_rankings = ranking_algorithm(target_job)
                st.subheader("Final Resume Rankings")
                st.write(df_resume_rankings)
            else:
                st.write("No files uploaded!")


if __name__ == "__main__":
    main()
