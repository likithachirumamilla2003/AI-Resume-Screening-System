from flask import Flask, render_template, request
from PyPDF2 import PdfReader

app = Flask(__name__)

skills_list = [

    # Programming Languages
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "typescript",
    "php",
    "ruby",
    "go",
    "swift",

    # Frontend
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "bootstrap",
    "tailwind css",

    # Backend
    "flask",
    "django",
    "node.js",
    "express.js",
    "spring boot",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",

    # AI / Data Science
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "power bi",

    # Cloud / DevOps
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "jenkins",
    "git",
    "github",

    # Tools
    "jira",
    "postman",
    "figma",
    "linux",
    "excel",

    # Cybersecurity
    "network security",
    "ethical hacking",

    # Mobile
    "android",
    "flutter",

    # Other
    "rest api",
    "graphql",
    "microservices"

]

@app.route("/", methods=["GET", "POST"])

def home():

    extracted_skills = []
    missing_skills = []
    score = 0

    if request.method == "POST":

        file = request.files["resume"]

        job_description = request.form["job_description"].lower()

        text = ""

        if file:

            pdf = PdfReader(file)

            for page in pdf.pages:
                text += page.extract_text().lower()

        # Extract skills from resume
        for skill in skills_list:

            if skill.lower() in text:

                extracted_skills.append(skill)

        # Find required skills from job description
        required_skills = []

        for skill in skills_list:

            if skill.lower() in job_description:

                required_skills.append(skill)

        # Find missing skills
        for skill in required_skills:

            if skill not in extracted_skills:

                missing_skills.append(skill)

        # Better Match Score Logic
        matched_skills = len(required_skills) - len(missing_skills)

        if len(required_skills) > 0:

            score = int(
                (matched_skills / len(required_skills)) * 100
            )

    return render_template(

        "index.html",

        skills=extracted_skills,

        missing=missing_skills,

        score=score

    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
