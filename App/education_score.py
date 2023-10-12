import spacy
from difflib import SequenceMatcher


def match_degrees_by_spacy(education_text, nlp):
    doc = nlp(education_text)
    degree_levels = []
    for ent in doc.ents:
        labels_parts = ent.label_.split("|")
        if labels_parts[0] == "DEGREE":
            # print((ent.text, ent.label_))
            if labels_parts[1] not in degree_levels:
                degree_levels.append(labels_parts[1])
    return degree_levels


def match_majors_by_spacy(education_text, nlp):
    doc = nlp(education_text)
    acceptable_majors = []
    for ent in doc.ents:
        labels_parts = ent.label_.split("|")
        if labels_parts[0] == "MAJOR":
            if labels_parts[2].replace("-", " ") not in acceptable_majors:
                acceptable_majors.append(labels_parts[2].replace("-", " "))
            if labels_parts[2].replace("-", " ") not in acceptable_majors:
                acceptable_majors.append(labels_parts[2].replace("-", " "))
    return acceptable_majors


# Function to extract degree level and field of study from education
def extract_education_info(df_resume, target_job):
    # Initialize the NLP pipeline and entity ruler
    nlp = spacy.load("en_core_web_sm")
    ruler = nlp.add_pipe("entity_ruler", before="ner")

    # Load the degree and major patterns
    ruler.from_disk("degrees_majors.jsonl")

    # Initialize lists to store the results
    resume_degrees = []
    resume_majors = []

    # Extract degree and major for each resume
    for education_text in df_resume["EDUCATION"]:
        degrees = match_degrees_by_spacy(education_text, nlp)
        majors = match_majors_by_spacy(education_text, nlp)
        resume_degrees.append(degrees)
        resume_majors.append(majors)

    # Extract degree and major for the target job
    job_degree = match_degrees_by_spacy(target_job["education"], nlp)
    job_major = match_majors_by_spacy(target_job["education"], nlp)

    (
        df_resume["education_degree"],
        df_resume["education_major"],
        target_job["education_degree"],
        target_job["education_major"],
    ) = (resume_degrees, resume_majors, job_degree, job_major)

    return resume_degrees, resume_majors, job_degree, job_major


# Define a mapping for degree levels
degree_mapping = {
    "BACHELOR": 1,
    "MASTER": 2,
    "PHD": 3,
}


def get_education_degree_score(resume_degrees, job_degree):
    # Apply the mapping to the list of degrees
    numerical_degrees = [
        [degree_mapping.get(degree, 0) for degree in degrees]
        for degrees in resume_degrees
    ]
    # Get the highest degree for each resume
    applicant_degrees = [
        max(degrees) if degrees else 0 for degrees in numerical_degrees
    ]

    # Convert the job degree to numerical form
    numerical_job_degree = [degree_mapping.get(degree, 0) for degree in job_degree]
    # Get the minimum degree required for the job
    min_degree_required = min(numerical_job_degree)

    degree_scores = []
    for applicant_degree in applicant_degrees:
        degree_score = 0

        if applicant_degree >= min_degree_required:
            degree_score = 0
        else:
            degree_score = min_degree_required - applicant_degree

        # smaller degree score means greater similarity (0 means exact)
        # the max_degree_score may be 2 (eg: phd vs bachelor)
        max_degree_score = 2
        # By dividing (max_score - degree_score) by max_score, you normalize the score to be between 0 and 1, where a higher score indicates better similarity.
        degree_score = (max_degree_score - degree_score) / max_degree_score

        degree_scores.append(degree_score)

    return degree_scores


# Function to calculate text similarity using SequenceMatcher
def calculate_education_major_similarity(str1, str2):
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def get_education_major_score(resume_majors, job_major):
    field_scores = []

    for resume_major in resume_majors:
        # Convert resume_major array to string separated by ' '
        applicant_major = " ".join(resume_major)
        field_score = 0
        similarities = [
            calculate_education_major_similarity(applicant_major, required_major)
            for required_major in job_major
        ]
        # Find max similarity score
        if similarities:
            field_score = max(similarities)
        field_scores.append(field_score)

    return field_scores


def get_education_score(df_resume, target_job):
    resume_degrees, resume_majors, job_degree, job_major = extract_education_info(
        df_resume, target_job
    )

    degree_scores = get_education_degree_score(resume_degrees, job_degree)
    field_scores = get_education_major_score(resume_majors, job_major)

    # Set weights for degree and field_of_study
    degree_weight = 0.7
    field_weight = 0.3

    combined_scores = [
        degree_weight * degree_score + field_weight * field_score
        for degree_score, field_score in zip(degree_scores, field_scores)
    ]

    df_resume["education_score"] = combined_scores
