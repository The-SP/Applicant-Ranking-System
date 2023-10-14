import io
import fitz
import pandas as pd


def extract_sections_from_pdf(readable_file, keywords):
    # Open the PDF with fitz
    doc = fitz.open(stream=readable_file, filetype="pdf")

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
                        if (
                            s["flags"] == 20 and s["text"].isupper()
                        ):  # check if the text is bold and uppercase
                            # This is a section title, so start a new section
                            current_section = s["text"]
                            sections[current_section] = ""
                        elif any(keyword == s["text"].upper() for keyword in keywords):
                            # The text contains a keyword, so start a new section
                            current_section = s["text"].upper()
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


# Define a list of common resume section titles
keywords = [
    "PROFILE",
    "SUMMARY",
    "ABOUT ME",
    "PERSONAL PROFILE",
    "PERSONAL SUMMARY",
    "WORK EXPERIENCE",
    "EXPERIENCE",
    "JOB HISTORY",
    "EMPLOYMENT HISTORY",
    "EDUCATION",
    "EDUCATIONAL BACKGROUND",
    "ACADEMIC HISTORY",
    "SKILLS",
    "ABILITIES",
    "COMPETENCIES",
    "EXPERTISE",
    "PROJECTS",
    "PORTFOLIO",
    "CERTIFICATIONS",
    "CREDENTIALS",
    "ACCREDITATIONS",
    "AWARDS",
    "HONORS",
    "ACHIEVEMENTS",
    "INTERESTS",
    "HOBBIES",
    "ACTIVITIES",
]

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
        "JOB HISTORY",
        "EMPLOYMENT HISTORY",
    ],
    "EDUCATION": ["EDUCATION", "EDUCATIONAL BACKGROUND", "ACADEMIC HISTORY"],
    "SKILLS": ["SKILLS", "ABILITIES", "COMPETENCIES", "EXPERTISE"],
    "PROJECTS": ["PROJECTS", "PORTFOLIO"],
    "CERTIFICATIONS": ["CERTIFICATIONS", "CREDENTIALS", "ACCREDITATIONS"],
    "AWARDS": ["AWARDS", "HONORS", "ACHIEVEMENTS"],
    "INTERESTS": ["INTERESTS", "HOBBIES", "ACTIVITIES"],
}

# Create a reverse mapping for easy lookup
keywords_section = {
    keyword: section
    for section, keywords in section_keywords.items()
    for keyword in keywords
}


def parse_resume_files(resume_files):
    # Initialize an empty list to hold the resumes
    resumes = []

    # Loop over each file
    for resume_file in resume_files:
        # Check if the file is a PDF
        if resume_file.name.endswith(".pdf"):
            print(f"Processing {resume_file.name}...")

            # Read the uploaded file into a bytes object
            resume_bytes = resume_file.read()

            # Create a readable file object
            readable_file = io.BytesIO(resume_bytes)

            sections = extract_sections_from_pdf(readable_file, keywords)
            new_sections = map_sections(sections, keywords_section)

            # Ensure that all section titles are present
            for section in section_keywords.keys():
                if section not in new_sections:
                    new_sections[section] = ""
                    
            # Add the filename to the dictionary
            new_sections["Filename"] = resume_file.name

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
