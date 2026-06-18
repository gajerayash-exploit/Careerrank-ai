from fpdf import FPDF
import os

OUTPUT_DIR = os.path.join("data", "sample_resumes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize(text):
    
    return (text
        .replace('\u2013', '-').replace('\u2014', '-')
        .replace('\u2018', "'").replace('\u2019', "'")
        .replace('\u201c', '"').replace('\u201d', '"')
        .encode('latin-1', errors='replace').decode('latin-1'))

def make_resume(filename, name, email, phone, summary, experience, skills, education):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 12, sanitize(name), new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"{sanitize(email)}  |  {sanitize(phone)}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    def section(title, body):
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(59, 130, 246)
        pdf.cell(0, 8, sanitize(title), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(59, 130, 246)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, sanitize(body))
        pdf.ln(4)

    section("Professional Summary", summary)
    section("Work Experience", experience)
    section("Technical Skills", skills)
    section("Education", education)

    path = os.path.join(OUTPUT_DIR, filename)
    pdf.output(path)
    print(f"  Created: {path}")

resumes = [
    {
        "filename": "alice_johnson_resume.pdf",
        "name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "phone": "+91-9876543210",
        "summary": (
            "Full-Stack Software Engineer with 5+ years of experience building scalable web "
            "applications using Python, Django, React, and AWS. Passionate about clean code, "
            "Agile methodologies, and delivering impactful products."
        ),
        "experience": (
            "Senior Software Engineer - TechCorp Pvt. Ltd. (2021 – Present)\n"
            "- Designed and deployed REST APIs using Python and Django serving 1M+ requests/day.\n"
            "- Migrated monolith to microservices architecture using Docker and Kubernetes.\n"
            "- Implemented CI/CD pipelines using Jenkins and GitHub Actions.\n"
            "- Worked closely with product managers in Agile/Scrum sprints.\n\n"
            "Software Engineer - StartupXYZ (2019 – 2021)\n"
            "- Built responsive frontends with React and JavaScript.\n"
            "- Managed PostgreSQL databases and wrote complex SQL queries.\n"
            "- Deployed applications on AWS EC2, S3, and RDS."
        ),
        "skills": (
            "Python, Django, Flask, React, JavaScript, Node.js, SQL, PostgreSQL, MySQL, "
            "AWS, Docker, Kubernetes, Git, GitHub, CI/CD, Jenkins, REST API, Agile, Scrum, "
            "Linux, Bash, Problem Solving, Teamwork, Communication"
        ),
        "education": "B.Tech in Computer Science - IIT Delhi (2019)  |  CGPA: 8.9/10",
    },
    {
        "filename": "bob_sharma_resume.pdf",
        "name": "Bob Sharma",
        "email": "bob.sharma@gmail.com",
        "phone": "+91-8765432109",
        "summary": (
            "Backend Developer with 3 years of experience in Python and Flask. "
            "Comfortable working with cloud platforms and relational databases. "
            "Seeking to grow in a product-driven engineering team."
        ),
        "experience": (
            "Backend Developer - DataSoft Solutions (2022 – Present)\n"
            "- Developed RESTful microservices using Python and Flask.\n"
            "- Optimised PostgreSQL queries reducing response time by 40%.\n"
            "- Deployed services on GCP Cloud Run and managed CI/CD via GitLab.\n\n"
            "Junior Developer - WebAgency (2021 – 2022)\n"
            "- Built simple CRUD applications with Python and SQL.\n"
            "- Used Git for version control and collaborated in small Agile teams."
        ),
        "skills": (
            "Python, Flask, Django, SQL, PostgreSQL, GCP, Docker, Git, GitHub, GitLab, "
            "REST API, Linux, Agile, Teamwork, Problem Solving"
        ),
        "education": "B.Tech in Information Technology - NIT Trichy (2021)  |  CGPA: 8.2/10",
    },
    {
        "filename": "carol_patel_resume.pdf",
        "name": "Carol Patel",
        "email": "carol.patel@outlook.com",
        "phone": "+91-7654321098",
        "summary": (
            "Frontend-focused developer with 2 years of experience in React and JavaScript. "
            "Familiar with basic Python scripting. Enthusiastic about UI/UX and building "
            "beautiful user interfaces."
        ),
        "experience": (
            "Frontend Developer - CreativeApps (2023 – Present)\n"
            "- Built responsive single-page applications using React and Tailwind CSS.\n"
            "- Collaborated with backend teams to integrate REST APIs.\n"
            "- Used Git and GitHub for version control.\n\n"
            "Intern - WebStudio (2022 – 2023)\n"
            "- Developed static websites using HTML, CSS, and JavaScript.\n"
            "- Basic experience with Bootstrap and jQuery."
        ),
        "skills": (
            "React, JavaScript, HTML, CSS, Tailwind, Bootstrap, Git, GitHub, REST API, "
            "Figma, Agile, Teamwork, Communication"
        ),
        "education": "B.Sc in Computer Science - Mumbai University (2022)  |  CGPA: 7.8/10",
    },
    {
        "filename": "david_krishna_resume.pdf",
        "name": "David Krishna",
        "email": "david.krishna@techmail.in",
        "phone": "+91-6543210987",
        "summary": (
            "DevOps Engineer with 4 years of experience in cloud infrastructure, containerisation, "
            "and automation. Expert in AWS, Docker, Kubernetes, and Terraform. Strong background "
            "in security and networking."
        ),
        "experience": (
            "DevOps Engineer - CloudSystems Inc. (2021 – Present)\n"
            "- Designed and maintained AWS infrastructure (EC2, RDS, S3, Lambda, VPC).\n"
            "- Managed Docker containers and Kubernetes clusters for 50+ microservices.\n"
            "- Built CI/CD pipelines using Jenkins and GitHub Actions.\n"
            "- Implemented security best practices, IAM policies, and SSL certificates.\n\n"
            "Systems Engineer - TechOps Ltd. (2020 – 2021)\n"
            "- Managed Linux servers and wrote shell scripts for automation.\n"
            "- Monitored system performance using Grafana and Prometheus."
        ),
        "skills": (
            "AWS, Azure, GCP, Docker, Kubernetes, Terraform, Jenkins, GitHub, CI/CD, "
            "Linux, Bash, Shell Scripting, Networking, Security, Cybersecurity, Python, "
            "Git, Agile, Problem Solving"
        ),
        "education": "B.Tech in Electronics - BITS Pilani (2020)  |  CGPA: 8.5/10",
    },
    {
        "filename": "eva_mehta_resume.pdf",
        "name": "Eva Mehta",
        "email": "eva.mehta@career.com",
        "phone": "+91-9123456780",
        "summary": (
            "Recent computer science graduate with internship experience in web development. "
            "Basic knowledge of Python and SQL. Looking to start my professional career in "
            "software engineering."
        ),
        "experience": (
            "Web Development Intern - LocalStartup (2024 – 3 months)\n"
            "- Assisted in building a company website using HTML, CSS, and Bootstrap.\n"
            "- Fixed minor bugs in a Python Flask application.\n"
            "- Participated in weekly team stand-ups."
        ),
        "skills": (
            "Python, HTML, CSS, Bootstrap, SQL, Git, Teamwork, Communication, "
            "Time Management, Problem Solving"
        ),
        "education": "B.Sc in Information Technology - Pune University (2024)  |  CGPA: 7.2/10",
    },
]

if __name__ == "__main__":
    print("Generating sample resumes...")
    for r in resumes:
        make_resume(**r)
    print(f"\nDone! {len(resumes)} resumes saved to '{OUTPUT_DIR}/'")
