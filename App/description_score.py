import re
import numpy as np

from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity


def clean_description(text):
    # Remove punctuation and numbers
    text = re.sub(r"[^a-zA-Z\+]", " ", text)
    # Remove extra blank spaces
    text = re.sub(r"\s+", " ", text).strip()
    # Convert to lowercase
    text = text.lower()
    return text


def preprocess_job(target_job):
    title, description, skills = (
        target_job["title"],
        target_job["description"],
        target_job["skills"],
    )
    # Clean description
    if skills:
        description = skills.replace(",", "") + " " + description
    if title:
        description = f"{title} {description}"
    description = clean_description(description)
    # print('Cleaned job description:', description)
    return description


def get_description_score(df_resume, target_job):
    # Load a pre-trained sentence transformer model
    MODEL_NAME = "all-MiniLM-L12-v2"
    model = SentenceTransformer(MODEL_NAME)

    # Combine text from all columns to get overall resume text
    df_resume["clean_resume_text"] = (
        df_resume[["PROFILE", "EXPERIENCE", "PROJECTS", "CERTIFICATIONS"]]
        .fillna(" ")
        .apply(lambda row: " ".join(row), axis=1)
        .apply(clean_description)
    )

    job_embeddings = model.encode(preprocess_job(target_job))
    # resume_embeddings = model.encode(df_resume['clean_resume_text'])

    resume_embeddings = np.zeros(
        (len(df_resume), model.get_sentence_embedding_dimension())
    )
    for i in tqdm(range(len(df_resume)), desc="Encoding resume texts", unit="resumes"):
        resume_embeddings[i] = model.encode(df_resume.iloc[i]["clean_resume_text"])

    # Calculate cosine similarity between the job description and resumes
    cosine_similarities = cosine_similarity(resume_embeddings, [job_embeddings])

    # Set negative scores to 0
    cosine_similarities[cosine_similarities < 0] = 0

    df_resume["description_score"] = cosine_similarities
