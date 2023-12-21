import os
import fitz
import pandas as pd

potential_section_titles = []

RESUME_PATH = "resumes/latex"


def extract_sections_from_pdf(pdf_path, keywords):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Initialize an empty dictionary to hold the sections
    sections = {}
    current_section = None

    # Loop over each page in the document
    for page in doc:
        # Extract the text as a dictionary
        blocks = page.get_text("dict")["blocks"]

        for b in blocks:  # iterate through the text blocks
            if "lines" in b:
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        # check if the text is bold and uppercase
                        if s["flags"] == 20 and s["text"].isupper():
                            """
                            This is to identify different new keywords that could be used as section titles by various resumes
                            """
                            if s["text"] not in keywords:
                                potential_section_titles.append(s["text"])
                            # # This is a section title, so start a new section
                            # current_section = s["text"]
                            # sections[current_section] = ""

                        if any(keyword == s["text"].strip().upper() for keyword in keywords):
                            # The text contains a keyword, so start a new section
                            current_section = s["text"].strip().upper()
                            sections[current_section] = ""
                        elif current_section is not None:
                            # This is not a section title, so append it to the current section
                            sections[current_section] += s["text"] + " "

    return sections


def map_sections(sections, keywords_section):
    # Map the collected section titles to new section titles
    new_sections = {}
    for section, text in sections.items():
        new_section = keywords_section.get(section)
        if new_section is not None:
            if new_section not in new_sections:
                new_sections[new_section] = text
            else:
                new_sections[new_section] += text
    return new_sections


# Define a dictionary of common resume section titles and their associated keywords
section_keywords = {
    "PROFILE": [
        "PROFILE",
        "SUMMARY",
        "ABOUT ME",
        "PERSONAL PROFILE",
        "PERSONAL SUMMARY",
    ],
    "EXPERIENCE": [
        "EXPERIENCE",
        "WORK EXPERIENCE",
        "PROFESSIONAL EXPERIENCE",
        "RELEVANT WORK EXPERIENCE",
        "JOB HISTORY",
        "EMPLOYMENT HISTORY",
    ],
    "EDUCATION": ["EDUCATION", "EDUCATIONAL BACKGROUND", "ACADEMIC HISTORY"],
    "SKILLS": [
        "SKILLS",
        "TECHNICAL SKILLS",
        "PROGRAMMING SKILLS",
        "ABILITIES",
        "COMPETENCIES",
        "EXPERTISE",
    ],
    "PROJECTS": ["PROJECTS", "PORTFOLIO"],
    "CERTIFICATIONS": ["CERTIFICATIONS", "CREDENTIALS", "ACCREDITATIONS"],
    "AWARDS": ["AWARDS", "HONORS", "ACHIEVEMENTS"],
    "INTERESTS": ["INTERESTS", "HOBBIES", "ACTIVITIES"],
}

# Create a list of all keywords from the section_keywords dictionary
keywords = [
    keyword for keyword_list in section_keywords.values() for keyword in keyword_list
]

# Create a reverse mapping for easy lookup
keywords_section = {
    keyword: section
    for section, keywords in section_keywords.items()
    for keyword in keywords
}

# Get a list of all the files in the 'resumes' directory
resume_files = os.listdir(RESUME_PATH)

# Initialize an empty list to hold the resumes
resumes = []

# Loop over each file
for filename in resume_files:
    # Check if the file is a PDF
    if filename.endswith(".pdf"):
        print(f"Processing {filename}...")
        pdf_path = os.path.join(RESUME_PATH, filename)

        sections = extract_sections_from_pdf(pdf_path, keywords)
        new_sections = map_sections(sections, keywords_section)

        # Add the filename to the dictionary
        new_sections["Filename"] = filename.replace('.pdf', '')

        # Ensure that all section titles are present
        for section in section_keywords.keys():
            if section not in new_sections:
                new_sections[section] = ""

        # Add the dictionary to the list
        resumes.append(new_sections)


print("Writing data to CSV...")
# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(resumes)
# Fill NaN values with empty strings
df = df.fillna("")
# Write the DataFrame to a CSV file
df.to_csv("resume_sections.csv", index=False)
print("Finished writing data to CSV.")


print("\nPotential Section Titles")
print("-" * 100)
print(potential_section_titles)
print("-" * 100)
