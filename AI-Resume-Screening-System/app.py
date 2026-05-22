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
    required_skills = []
    score = 0
    text = ""

    if request.method == "POST":

        # Get uploaded resume
        file = request.files.get("resume")

        # Get job description
        job_description = request.form.get(
            "job_description", ""
        ).lower()

        # Check file uploaded
        if file and file.filename != "":

            try:

                # Read PDF directly
                pdf = PdfReader(file)

                # Extract text from all pages
                for page in pdf.pages:

                    extracted_text = page.extract_text()

                    if extracted_text:
                        text += extracted_text.lower()

            except Exception as e:

                print("Error reading PDF:", e)

        # Extract skills from resume
        for skill in skills_list:

            if skill in text:

                extracted_skills.append(skill)

        # Extract required skills from job description
        for skill in skills_list:

            if skill in job_description:

                required_skills.append(skill)

        # Find missing skills
        for skill in required_skills:

            if skill not in extracted_skills:

                missing_skills.append(skill)

        # Calculate match score
        if len(required_skills) > 0:

            matched_skills = (
                len(required_skills) - len(missing_skills)
            )

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
    app.run(debug=True)
