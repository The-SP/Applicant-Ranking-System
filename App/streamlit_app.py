import streamlit as st
import pandas as pd

from resume_parse import parse_resume_files
from applicant_ranking import ranking_algorithm


def main():
    st.title("Applicant Ranking System")

    # Set default values
    default_data = {
        "title": "Software Developer",
        "description": "Required skilled web developer.",
        "skills": "Python, Django, Django Rest, React, Javascript",
        "education": "Bachelor in Computer Engineering",
        "experience": "2 years",
    }

    # Job Description Inputs
    st.subheader("Job Description")
    title = st.text_input("Title", default_data["title"])
    description = st.text_input("Description", default_data["description"])
    skills = st.text_input("Skills", default_data["skills"])
    education = st.text_input("Education", default_data["education"])
    experience = st.text_input("Experience", default_data["experience"])

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
    if target_job:  #  check if it is not empty dictionary
        # Convert the dictionary to a Series
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
