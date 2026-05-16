
from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Fixed the missing comma below
SKILLS = [
    "python",
    "java",
    "flask",
    "html",
    "css",
    "javascript",
    "sql",
    "machine learning",  #  Fixed
    "react",
    "mongodb",
    "git"
]

# Extract text directly from the uploaded file stream
def extract_pdf_text(file_stream):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_stream)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

# Analyze Resume + Job Description
def analyze_resume(resume_text, job_text):
    resume_lower = resume_text.lower()
    job_lower = job_text.lower()

    # Skills found in resume
    found_skills = [skill for skill in SKILLS if skill in resume_lower]

    # Matching skills
    matched_skills = [skill for skill in SKILLS if skill in resume_lower and skill in job_lower]

    # Missing skills
    missing_skills = [skill for skill in SKILLS if skill in job_lower and skill not in resume_lower]

    # Score (capped at 100 max)
    score = min(len(matched_skills) * 20, 100)

    if score >= 80:
        level = "Excellent Match"
    elif score >= 50:
        level = "Good Match"
    else:
        level = "Low Match"

    # Recommended role
    if "python" in matched_skills:
        role = "Python Developer"
    elif "java" in matched_skills:
        role = "Java Developer"
    else:
        role = "General IT Role"

    # Converting lists to nice, readable comma-separated strings for HTML
    return (
        ", ".join(found_skills) if found_skills else "None",
        ", ".join(matched_skills) if matched_skills else "None",
        ", ".join(missing_skills) if missing_skills else "None",
        score,
        level,
        role
    )

# Home page
@app.route('/')
def home():
    return render_template("index.html", score=None)

# Analyze Route
@app.route('/analyze', methods=['POST'])
def analyze():
    # Get uploaded file
    file = request.files['resume']
    # Get job description
    job_text = request.form['job_text']

    if not file or file.filename == '':
        return "No file uploaded", 400

    # Pass the file stream straight into the extractor 
    resume_text = extract_pdf_text(file)

    # Analyze
    (
        skills,
        matched_skills,
        missing_skills,
        score,
        level,
        role
    ) = analyze_resume(resume_text, job_text)

    # Send results to HTML
    return render_template(
        "index.html",
        skills=skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        score=score,
        level=level,
        role=role
    )

if __name__ == "_main_":
    app.run(debug=True)