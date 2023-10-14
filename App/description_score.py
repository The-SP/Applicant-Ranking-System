import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_description(text):
    # Remove punctuation and numbers
    text = re.sub(r"[^a-zA-Z\+]", " ", text)
    # Convert to lowercase
    text = text.lower()
    return text


def preprocess_job(target_job):
    title, description, skills = (
        target_job['title'],
        target_job['description'],
        target_job['skills'],
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
    # Combine text from all columns to get overall resume text
    df_resume["clean_resume_text"] = (
        df_resume[["PROFILE", "EXPERIENCE", "PROJECTS", "CERTIFICATIONS"]]
        .fillna(" ")
        .apply(lambda row: " ".join(row), axis=1)
        .apply(clean_description)
    )

    # Initialize the TfidfVectorizer
    # min_df=3 means ignore terms that appear in less than 3 document
    tfidf_vectorizer = TfidfVectorizer(stop_words="english", min_df=3)

    # fit_transform the vectorizers and create tfidf matrix
    tfidf_matrix = tfidf_vectorizer.fit_transform(
        [preprocess_job(target_job)] + df_resume["clean_resume_text"].values.tolist()
    )

    # Calculate cosine similarity between the job description and resumes
    cosine_similarities = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:]
    ).flatten()

    df_resume["description_score"] = cosine_similarities
