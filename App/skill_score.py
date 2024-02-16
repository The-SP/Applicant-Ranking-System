from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
import re


# Helper function to check if a skill is present in the resume description
def skill_present(skill, description):
    # Use regular expression pattern matching to match the whole word
    pattern = r"\b" + re.escape(skill) + r"\b"
    return bool(re.search(pattern, description, re.IGNORECASE))


def vectorize_skills(df_resume_texts, target_job):
    # Remove '.js' extension from the skill to handle cases like 'react.js' and 'react'
    target_job_skills_text = target_job['skills'].replace('.js', '')
    # The 'skills' column has string values. Each string has skills sepearated by comma. So convert them to array of skills.
    target_job_skills = target_job_skills_text.lower().split(", ")
    # Initialize the MultiLabelBinarizer
    mlb = MultiLabelBinarizer(classes=target_job_skills)

    # Create a list of skills for each applicant's project
    applicant_skills_vector = df_resume_texts.apply(
        lambda x: [skill for skill in target_job_skills if skill_present(skill, x)]
    )

    # Use the MultiLabelBinarizer to transform the 'skills' column into binary vectors
    applicant_binary_vectors = mlb.fit_transform(applicant_skills_vector)

    return applicant_binary_vectors.tolist()


def get_skills_score(df_resume, target_job):
    df_resume["skills_vector"] = vectorize_skills(df_resume["SKILLS"], target_job)
    target_job["skills_vector"] = np.ones(len(target_job["skills"].split(", ")))

    target_vector = np.array(target_job["skills_vector"]).reshape(1, -1)
    applicant_vector = np.array(df_resume["skills_vector"].tolist())
    similarity_scores = cosine_similarity(target_vector, applicant_vector)
    df_resume["skills_score"] = similarity_scores.flatten()

    # target_vector is created from target_job['skills_vector']. It's reshaped to a 2D array with reshape(1, -1) because cosine_similarity expects a 2D array.
    # applicant_vectors is created by converting df_resume['skills_vector'] to a NumPy array using tolist(). This is done because cosine_similarity expects a 2D array.


def get_projects_score(df_resume, target_job):
    # Convert applicant projects into binary feature vectors
    df_resume['projects_vector'] = vectorize_skills(df_resume['PROJECTS'], target_job)

    target_vector = np.array(target_job['skills_vector']).reshape(1, -1)
    applicant_vector = np.array(df_resume['projects_vector'].tolist())
    similarity_scores = cosine_similarity(target_vector, applicant_vector)
    df_resume['projects_score'] = similarity_scores.flatten()