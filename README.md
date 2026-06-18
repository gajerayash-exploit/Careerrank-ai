# CareerRank AI 2.0 🎯
### Intelligent Recruitment SaaS & AI Candidate Screening Platform

> **"Rank the right talent with AI in seconds. Now powered by Gemini Pro & Supabase."**

---

## 📌 Overview

**CareerRank AI** is a production-grade HR-tech web application built with Python and Streamlit. It accepts a Job Description (JD) and multiple candidate resume PDFs, performs multi-layered NLP analysis, and returns a ranked leaderboard of candidates. 

**Version 2.0** introduces a massive architectural upgrade including Optical Character Recognition (OCR) for scanned resumes, Generative AI for custom interview questions, Supabase database integration for historical tracking, and an automated emailing system UI.

---

## ✨ Advanced Features (v2.0)

| Feature | Description |
|---|---|
| 🤖 **Generative AI Interviews** | Integrates **Google Gemini Pro** to analyze a candidate's "Missing Skills" and auto-generate 2 highly targeted, tough-but-fair technical interview questions. |
| 👁️ **Scanned Document OCR** | Uses `pytesseract` to detect and extract text from image-based/scanned PDFs when standard text extraction fails. |
| 🗄️ **Supabase Integration** | Connects to a cloud PostgreSQL database via Supabase to securely save and load historical candidate rankings and JDs. |
| ✉️ **Automated Email UI** | A seamless, single-click interface to simulate sending automated interview invitations or rejection emails directly from the dashboard. |

## 🧠 Core Features (v1.0)

| Feature | Description |
|---|---|
| 📄 **PDF Resume Parsing** | Extracts text from uploaded PDF resumes using `pdfplumber`. |
| 🔍 **NLP & Skill Extraction** | Lowercasing, lemmatisation, and matching 60+ industry skills via `spaCy` & `NLTK`. |
| 📊 **TF-IDF Similarity** | Vectorises JD and resume text; computes cosine similarity. |
| ⚖️ **Weighted Scoring** | `60% TF-IDF + 25% Skill Overlap + 15% Keyword Density`. |
| 🚫 **Missing Skill Penalty** | Deducts points if >50% of JD skills are absent. |
| 🏆 **Top 3 Spotlight** | Glassmorphism UI displaying Gold / Silver / Bronze medals. |
| ☁️ **Skill Word Cloud** | Visual word cloud of matched JD/resume skills using Matplotlib. |
| 📄 **Automated PDF Reports** | Generates a multi-page, branded recruiter report with methodology, rankings, and AI insights using `fpdf2`. |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit + Custom CSS (Glassmorphism & Responsive Grids) |
| **NLP Engine** | spaCy (`en_core_web_sm`), NLTK |
| **Generative AI** | Google Gemini (`google-generativeai`) |
| **Database** | Supabase (`supabase` Python Client) |
| **OCR Vision** | Tesseract OCR (`pytesseract`, `pdf2image`) |
| **Vectorisation** | scikit-learn TF-IDF |
| **PDF Export** | fpdf2 |
| **Language** | Python 3.10+ |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/careerrank-ai.git
cd careerrank-ai
```

### 2. Install OS Dependencies (For OCR)
**Linux / Streamlit Cloud:**
*Handled automatically by `packages.txt`*
```bash
sudo apt-get install tesseract-ocr poppler-utils
```
**Windows:** Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run app.py
```

### 5. Setup Keys (In-App)
Once the app is running (http://localhost:8501), open the left sidebar to enter your:
- **Gemini API Key** (for interview questions)
- **Supabase URL & Key** (for database history)

---

## 🧮 Scoring Formula

```text
Final Score = (TF-IDF × 0.60) + (Skill Overlap × 0.25) + (Keyword Density × 0.15)
            × 100

            + Education Bonus  (0 – 5 pts)
            + Experience Bonus (0 – 5 pts)
            − Missing Skill Penalty (if >50% skills missing)
            − Length Penalty (if resume < 200 characters)

Capped at 100 points.
```

---

## 👨‍💻 Built For

> **Elevate Labs Internship Project**  
> A real-world HR-tech SaaS demo showcasing applied NLP, Generative AI, Cloud Databases, modern UI/UX, and advanced Python software engineering.

---

## 📄 License

MIT License — free to use, modify, and distribute.
