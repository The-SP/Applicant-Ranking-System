import re
import spacy
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime


# Function to extract years of exp from job description
def extract_min_experience(text):
    # Define the regular expression patterns
    pattern_months = r"(\d+)(?=\s*month)"
    pattern_years = r"(\d+)(?=\s*year)"

    # Use search to get the first match
    match_years = re.search(pattern_years, text)
    match_months = re.search(pattern_months, text)

    # If a match was found, convert it to an integer and return
    if match_years:
        return int(match_years.group())
    elif match_months:
        return int(match_months.group()) / 12  # Convert months to years

    # If no match was found, return None
    return 0


def create_nlp_for_experience():
    nlp = spacy.load("en_core_web_sm")

    # Most of the date patterns are detected by default DATE entity
    # Define the pattern for '05/2015 - 06/2017' and '10/2020 - Present'.
    patterns = [
        # 05/2015 - 06/2017
        {"label": "DATE", "pattern": [{"SHAPE": "dd/dddd"}, {"TEXT": "-"}, {"SHAPE": "dd/dddd"}]},

        # 10/2020 - Present
        {"label": "DATE", "pattern": [{"SHAPE": "dd/dddd"}, {"TEXT": "-"}, {"LOWER": "present"}]},
        {"label": "DATE", "pattern": [{"SHAPE": "dd/dddd"}, {"TEXT": "-"}, {"LOWER": "current"}]},

        # Jan 2020 - current, March 2018 - Present
        {"label": "DATE", "pattern": [{"LOWER": {"in": ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]}}, {"TEXT": {"REGEX": "^\d{4}$"}}, {"TEXT": "-"}, {"LOWER": {"in": ["current", "present"]}}]},

        # 2020 - current
        {"label": "DATE", "pattern": [{"SHAPE": "dddd"}, {"TEXT": "-"}, {"LOWER": {"in": ["current", "present"]}}]},
        ]

    ruler = nlp.add_pipe("entity_ruler", before="ner")
    # Add the pattern to the ruler
    ruler.add_patterns(patterns)

    return nlp


def extract_years(dates):
    years = 0
    for date in dates:
        # Check if the date is in the "start - end" format
        if " - " not in date:
            continue

        # Split the date range into start and end dates
        start_date, end_date = date.split(" - ")

        # Replace 'Present' or 'current' with today's date
        if 'present' in end_date.lower() or 'current' in end_date.lower():
            end_date = datetime.today().strftime("%m/%Y")

        # Parse the dates
        start_date = parser.parse(start_date)
        end_date = parser.parse(end_date)

        # Calculate the difference in years (considering months)
        diff = relativedelta(end_date, start_date)
        years += round(diff.years + diff.months / 12, 2)

    return years


def get_experience_score(df_resume, target_job):
    target_job_experience = extract_min_experience(target_job["experience"])

    nlp = create_nlp_for_experience()

    experience_date_vectors = []
    # Calculate similarity scores for each applicant
    applicant_scores = []
    for applicant_experience in df_resume["EXPERIENCE"]:
        doc = nlp(applicant_experience)

        # Extract the dates
        extracted_dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
        experience_date_vectors.append(extracted_dates)

        applicant_years = extract_years(extracted_dates)

        if target_job_experience == 0:  # no experience requireed
            similarity_score = 1.0
        else:
            similarity_score = min(applicant_years / target_job_experience, 1.0)
        applicant_scores.append(similarity_score)

    df_resume["experience_dates"] = experience_date_vectors
    df_resume["experience_score"] = applicant_scores
