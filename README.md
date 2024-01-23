# Applicant Ranking System

## Description

The Applicant Ranking System is a tool designed to assist in the evaluation and ranking of job applicants based on their submitted resumes. This system leverages data extracted from resumes, including education, experience, skills, and projects, to provide an objective assessment of each candidate's suitability for a specific job role. The scoring process involves a comparison between the qualifications outlined in the job description and the information provided in the resumes.

## Problem Statement

In today's competitive job market, organizations receive a large volume of resumes for every open position. Manual resume screening is a time-consuming and resource-intensive task for recruiters and HR professionals.
This application aims to automate the screening process, effectively filtering out irrelevant resumes and allowing recruiters to focus their time and efforts on the most qualified candidates.

## Getting Started

1. **Download and Use the App**:

   - To get started, download the project and navigate to the `App` folder. Run the Streamlit app using the following command:
     ```
     streamlit run streamlit_app.py
     ```
   - This will launch the web-based interface for the Applicant Ranking System.

2. **Experimenting with Resume Parsing and Scoring Models**:

   - For advanced users, you can experiment with the resume parsing and scoring models using Jupyter notebooks: `Resume Parser/resume_parser.ipynb` and `Resume Parser/resume_score.ipynb`.

3. **Project Directory Overview**

   - For a detailed overview of the project's directory structure, please refer to [folders_overview.md](folders_overview.md).

## Usage

To use the Streamlit App, follow these steps:

1. **Provide Job Description**:

   - Start by entering the job title and description for the position you're hiring for. This description will be used as a reference to evaluate applicants.

2. **Set Feature Weights**:

   - Specify the importance or weightage for various parameters such as education, experience, skills, and projects. These weights determine the significance of each feature in the evaluation process. Ensure that the sum of weights is always equal to 1.

3. **Upload Applicants' Resumes**:

   - Click on the "Upload Applicant's Resumes" button to upload the resumes of the applicants. The system accepts resumes in PDF format.

4. **Parse and Evaluate**:

   - Click the "Parse Resume" button to initiate the evaluation process. The system will extract relevant information from the uploaded resumes and perform a comparative analysis against the provided job description.

5. **View Rankings**:
   - Once the evaluation is complete, the system will display the rankings of the applicants. A detailed breakdown of scores for each feature will be provided.

# Algorithm Overview

### Data Extraction and Parsing

- The resume parser uses the `pymupdf` library to convert the resumes from PDF format to plain text. Next, the parser organizes the content into distinct sections, each corresponding to a key aspect of the candidate's qualifications. These sections typically include educational background, work experience, skills, and completed projects.

- To determine a section title, the resume parser checks if it fulfills all 3 following conditions:

      - It is the only text item in the line
      - It is bolded
      - Its letters are all UPPERCASE

  Using the above technique, an evaluation of many resumes was conducted to identify the most common resume section keywords, which were then compiled into a list.

- During the actual resume parsing, the system utilizes a curated list of common resume section title keywords. When a match is found, the corresponding section is extracted and processed.

### Score Calculation

Each section (education, experience, skills, projects, description) is evaluated against the job description. Scores are assigned based on the extent of match between the resume and job requirements.

1. **Description**  
We use pre-trained sentence transformer models to calculate the similarity between the resume description and the job description.
By using sentence embeddings, our description comparison captures contextual information and semantic relationships.

2. **Education**

- Identify degree and major in education  
  Our system uses Spacy library to extract information (degree and major) from Education section. We prepared a dictionary that has common education degrees and majors related to computer engineering field. We fed that dictionary to the Spacy rule-based EntityRuler in order to detect and recognize entities in our job description.
- Evaluation

    1. Degree Evaluation:

    - Different degree levels are assigned corresponding values (e.g., Bachelor=1, Master=2, PhD=3).
    - If the highest degree in a resume is greater than or equal to the required minimum job degree, the score is 1,
    - Otherwise, it is calculated using a formula that considers the difference between the degrees.

    2. Field of Study Evaluation:

    - The field of study (major) is divided into three parts. Each part of the major represents a level of specificity in the field of study. This allows for partial matches to be considered in a structured manner.
    - A similarity score is assigned based on partial matches in the 1st, 2nd, and 3rd parts of the major.

    3. Combining Degree and Field Scores:  
       The degree score is weighted by 0.7, and the field score is weighted by 0.3 to calculate total education score.

4. **Experience**

- Extracts the 'X years' part from the target job experience.
- Calculates similarity scores for each applicant's experience, taking the ratio of their 'X years' to the target job's 'X years'.
- The score is limited it to a maximum of 1.0 to avoid giving excessive credit to applicants with more experience than needed.

4. **Skills**

- Binary vectors are generated for each applicant, representing the presence (1) or absence (0) of specific skills from the target job in the applicant's skill set, utilizing the 'MultiLabelBinarizer'.
- The system then calculates the similarity between the skill vectors of the applicant and the target job.

5.  **Projects**  
    _It checks if the applicant has made at least one project using the required skills or not._

    1. A specialized check is performed to verify if a skill is present in the project description using regular expression pattern matching to identify complete word matches.

    2. The vectorization process involves converting project descriptions into binary feature vectors. For each applicant, it iterates over the required skills and checks if any of them are present in the project descriptions.

    3. Using cosine similarity, the system calculates the similarity score between the job_skills_vector and each applicant's project vector. This score indicates how closely the applicant's projects match the required job skills.
