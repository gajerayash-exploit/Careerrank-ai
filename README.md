# CareerRank AI 🎯
### Intelligent Resume Ranking & Candidate Screening Platform

> **"Rank the right talent with AI in seconds."**

---

## 📌 Overview

**CareerRank AI** is a production-style HR-tech web application built with Python and Streamlit. It accepts a Job Description (JD) and multiple candidate resume PDFs, performs multi-layered NLP analysis, and returns a ranked leaderboard of candidates — complete with matched/missing skills, AI insights, keyword highlighting, and downloadable reports.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **PDF Resume Parsing** | Extracts text from uploaded PDF resumes using `pdfplumber` |
| 🧠 **NLP Preprocessing** | Lowercasing, lemmatisation, stopword removal via `spaCy` / `NLTK` |
| 🔍 **Skill Extraction** | Matches 60+ industry skills against a curated knowledge base |
| 📊 **TF-IDF Similarity** | Vectorises JD and resume text; computes cosine similarity |
| ⚖️ **Weighted Scoring** | `60% TF-IDF + 25% Skill Overlap + 15% Keyword Density` |
| 🎓 **Education Bonus** | Detects degree level (B.Tech → PhD) and adds bonus points |
| 🗓️ **Experience Bonus** | Detects years of experience and rewards seniority |
| 🚫 **Missing Skill Penalty** | Deducts points if >50% of JD skills are absent |
| 👤 **Candidate NER** | Extracts name, email, and phone from resume text (regex-based) |
| 🏆 **Top 3 Spotlight** | Gold / Silver / Bronze spotlight for the top candidates |
| 🔦 **JD Keyword Highlighting** | Resume text preview with JD keywords highlighted in-app |
| ☁️ **Skill Word Cloud** | Visual word cloud of matched JD/resume skills |
| 📥 **CSV Export** | Download full ranked results as a spreadsheet |
| 📄 **PDF Report** | Branded recruiter report with abstract, steps, rankings & conclusion |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit + custom CSS (Glassmorphism) |
| NLP Engine | spaCy (`en_core_web_sm`), NLTK |
| Vectorisation | scikit-learn TF-IDF |
| Similarity | Cosine Similarity |
| PDF Parsing | pdfplumber |
| Charts | Plotly |
| Word Cloud | wordcloud + matplotlib |
| PDF Export | fpdf2 |
| Language | Python 3.10+ |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/careerrank-ai.git
cd careerrank-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download NLP Models
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt_tab')"
```

### 4. Run the App
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 📁 Project Structure

```
Project_Resume_Builder/
│
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── utils/
│   ├── nlp_engine.py          # Core NLP: extraction, scoring, highlighting
│   ├── ui_components.py       # Custom CSS, hero, cards, spotlight
│   └── pdf_generator.py       # Branded PDF report generator
│
├── data/
│   ├── sample_jd.txt          # Sample Job Description for testing
│   └── sample_resumes/        # Sample PDF resumes for demo
│
└── .streamlit/
    └── config.toml            # Streamlit theme configuration
```

---

## 🧮 Scoring Formula

```
Final Score = (TF-IDF × 0.60) + (Skill Overlap × 0.25) + (Keyword Density × 0.15)
            × 100

            + Education Bonus  (0 – 5 pts)
            + Experience Bonus (0 – 5 pts)
            − Missing Skill Penalty (if >50% skills missing)
            − Length Penalty (if resume < 200 characters)

Capped at 100 points.
```

| Score Range | Recommendation |
|---|---|
| 75 – 100 | ✅ Strong match — shortlist |
| 50 – 74 | ⚠️ Moderate match — review manually |
| 0 – 49 | ❌ Low match — not recommended |

---

## 📋 Output Format

Each ranked candidate card displays:

- **Rank** (1 = best match)
- **Candidate Name** (auto-extracted)
- **Email & Phone** (auto-extracted)
- **Match Score** (0–100%)
- **Recommendation** label
- **AI Insight** — why this candidate matches
- **Matched Skills** — skills found in both JD and resume
- **Missing Core Skills** — JD skills absent from resume
- **JD Keyword Preview** — resume text with JD terms highlighted

---

## 📦 Requirements

```
streamlit
spacy
nltk
scikit-learn
pdfplumber
plotly
pandas
fpdf2
wordcloud
matplotlib
```

---

## 👨‍💻 Built For

> **Elevate Labs Internship Project**  
> A real-world HR-tech SaaS demo showcasing applied NLP, modern UI/UX, and Python engineering.

---

## 📄 License

MIT License — free to use, modify, and distribute.
