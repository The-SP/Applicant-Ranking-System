import spacy


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
            acceptable_majors.append(labels_parts[1:])
    return acceptable_majors


# Function to extract degree level and field of study from education
def extract_education_info(df_resume, target_job):
    # Initialize the NLP pipeline and entity ruler
    nlp = spacy.load("en_core_web_sm")
    # Disable the default 'ner' component
    nlp.disable_pipe("ner")
    # Add the pattern to the matcher
    PATTERN_PATH = "degrees_majors.jsonl"
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    # Load the degree and major patterns
    ruler.from_disk(PATTERN_PATH)

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


"""
# The major is divided into three parts: 1st part, 2nd part, and 3rd part. Each part of the major represents a level of specificity in the field of study.
# By breaking down the major into these parts, the code attempts to capture a hierarchy of specificity, allowing for partial matches to be considered in a structured manner. 
# A similarity score is assigned based on partial matches in the 1st, 2nd, and 3rd parts of the major.
Example:
    job_major = ['CS', 'AI', 'machine-learning']
    resume_major = [['CS', 'CS', 'computer-science'], ['CS', 'AI', 'data-science']]
    # Output: Major Score: 0.6 (based on the partial match in the 2nd part i.e. 'AI')
"""


def calculate_education_major_similarity(resume_major, job_major):
    score = 0.0
    for major in resume_major:
        # Check for an exact match in the 3rd part
        if job_major[2] == major[2]:
            score = 1.0  # max_score reached
            break
        # Check for a match in the 2nd part
        elif job_major[1] == major[1]:
            score = max(score, 0.6)
        # Check for a match in the 1st part
        elif job_major[0] == major[0]:
            score = max(score, 0.3)
    return score


def get_education_major_score(resume_majors, job_major):
    field_scores = []

    for resume_major in resume_majors:
        field_score = 0
        similarities = [
            calculate_education_major_similarity(resume_major, required_major)
            for required_major in job_major
        ]
        # Find max similarity score
        if similarities:
            field_score = max(similarities)
        field_scores.append(field_score)

    return field_scores


"""
Function to calculate degree score:
- It maps degree levels to numerical values, finds the highest degree for each resume,
- Converts the job degree to numerical form, and calculates a degree score based on a scoring formula.
- If the highest degree in a resume is greater than or equal to the minimum job degree, the score is 1,
- Otherwise, it is calculated using a formula that considers the difference between the degrees.
"""

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
            degree_score = 1
        else:
            degree_score = 1 - (min_degree_required - applicant_degree) / max(
                min_degree_required, 1
            )

        degree_scores.append(degree_score)

    return degree_scores


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
