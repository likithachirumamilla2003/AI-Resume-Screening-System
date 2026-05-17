from flask import Flask, render_template, request
from PyPDF2 import PdfReader

app = Flask(__name__)

skills_list = [
    "python",
    "java",
    "sql",
    "html",
    "css",
    "javascript",
    "flask",
    "machine learning",
    "power bi",
    "aws",
    "git",
    "github"
]

@app.route("/", methods=["GET", "POST"])
def home():

    extracted_skills = []
    missing_skills = []
    match_score = 0

    if request.method == "POST":

        resume = request.files["resume"]

        job_description = request.form["job_description"]

        if resume.filename != "":

            file_path = "uploads/" + resume.filename

            resume.save(file_path)

            pdf = PdfReader(file_path)

            text = ""

            for page in pdf.pages:

                extracted_text = page.extract_text()

                if extracted_text:

                    text += extracted_text

            text = text.lower()

            for skill in skills_list:

                if skill.lower() in text:

                    extracted_skills.append(skill)

            job_description = job_description.lower()

            required_skills = []

            for skill in skills_list:

                if skill.lower() in job_description:

                    required_skills.append(skill)

            matched_skills = 0

            for skill in required_skills:

                if skill in extracted_skills:

                    matched_skills += 1

                else:

                    missing_skills.append(skill)

            if len(required_skills) > 0:

                match_score = int(
                    (matched_skills / len(required_skills)) * 100
                )

    return render_template(
        "index.html",
        skills=extracted_skills,
        score=match_score,
        missing=missing_skills
    )

app.run(debug=True)