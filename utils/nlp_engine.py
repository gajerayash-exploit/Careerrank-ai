import re
import spacy
import nltk
from nltk.corpus import stopwords
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    nlp = spacy.load('en_core_web_sm')
except Exception:
    nlp = None  

COMMON_SKILLS = [
    'python', 'java', 'c++', 'javascript', 'react', 'node.js', 'angular', 'vue',
    'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'aws', 'azure', 'gcp',
    'docker', 'kubernetes', 'ci/cd', 'jenkins', 'git', 'github', 'gitlab',
    'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow',
    'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
    'data analysis', 'data visualization', 'tableau', 'power bi', 'excel',
    'agile', 'scrum', 'kanban', 'jira', 'confluence', 'communication',
    'leadership', 'problem solving', 'teamwork', 'time management', 'project management',
    'html', 'css', 'tailwind', 'bootstrap', 'django', 'flask', 'fastapi',
    'rest api', 'graphql', 'microservices', 'system design', 'c#', '.net',
    'ruby', 'ruby on rails', 'php', 'laravel', 'golang', 'rust', 'scala',
    'linux', 'bash', 'shell scripting', 'networking', 'security', 'cybersecurity'
]

EDUCATION_KEYWORDS = {
    'phd': 10, 'doctorate': 10,
    'mtech': 8, 'm.tech': 8, 'msc': 7, 'm.sc': 7, 'mba': 8, 'master': 7,
    'btech': 5, 'b.tech': 5, 'bsc': 4, 'b.sc': 4, 'bachelor': 4, 'be': 4,
    'diploma': 2, '12th': 1, 'high school': 1
}

def extract_text_from_pdf(pdf_file):
    
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"[PDF ERROR] {e}")
    return text

def preprocess_text(text):
    
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    if nlp:
        doc = nlp(text[:100000])  
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_space and len(token.text) > 1]
        return " ".join(tokens)
    else:
        try:
            stop_words = set(stopwords.words('english'))
        except Exception:
            stop_words = set()
        tokens = nltk.word_tokenize(text)
        return " ".join([w for w in tokens if w not in stop_words])

def extract_skills(text):
    
    found = set()
    text_lower = text.lower()
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.add(skill)
    return list(found)

def extract_candidate_info(text):
    
    info = {'name': 'N/A', 'email': 'N/A', 'phone': 'N/A'}

    email_match = re.search(r'[\w.\-+]+@[\w\-]+\.[a-zA-Z]{2,}', text)
    if email_match:
        info['email'] = email_match.group(0)

    phone_match = re.search(
        r'(\+?\d{1,3}[\s\-]?)?(\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{4}', text
    )
    if phone_match:
        info['phone'] = phone_match.group(0).strip()

    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:8]:  
        
        if re.match(r'^[A-Za-z]+([\s][A-Za-z]+){1,3}$', line) and len(line) < 50:
            info['name'] = line.title()
            break

    return info

def detect_education_level(text):
    
    text_lower = text.lower()
    max_score = 0
    for keyword, score in EDUCATION_KEYWORDS.items():
        if keyword in text_lower:
            max_score = max(max_score, score)
    
    return round((max_score / 10) * 5, 2)

def detect_experience_years(text):
    
    text_lower = text.lower()
    years = 0
    
    matches = re.findall(r'(\d+)\+?\s*(?:to\s*\d+\s*)?years?\s*(?:of\s*)?(?:experience|exp)?', text_lower)
    if matches:
        years = max(int(y) for y in matches)
    
    bonus = min(years, 5)
    return float(bonus)

def calculate_keyword_density(resume_text, jd_skills):
    
    if not jd_skills or not resume_text:
        return 0.0
    text_lower = resume_text.lower()
    hits = sum(1 for skill in jd_skills if re.search(r'\b' + re.escape(skill) + r'\b', text_lower))
    return hits / len(jd_skills)

def highlight_jd_keywords(resume_text, jd_skills):
    
    preview = resume_text[:1500].replace('<', '&lt;').replace('>', '&gt;')
    for skill in sorted(jd_skills, key=len, reverse=True):  
        pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
        preview = pattern.sub(
            f'<mark style="background:rgba(59,130,246,0.35);color:#F8FAFC;'
            f'border-radius:3px;padding:1px 4px;">{skill}</mark>',
            preview
        )
    return preview.replace('\n', '<br>')

def analyze_resume(resume_text, jd_text):
    
    resume_clean = preprocess_text(resume_text)
    jd_clean = preprocess_text(jd_text)

    vectorizer = TfidfVectorizer()
    try:
        vectors = vectorizer.fit_transform([jd_clean, resume_clean])
        tfidf_score = float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0])
    except ValueError:
        tfidf_score = 0.0

    jd_skills = set(extract_skills(jd_text))
    resume_skills = set(extract_skills(resume_text))
    matched_skills = jd_skills & resume_skills
    missing_skills = jd_skills - resume_skills

    if len(jd_skills) > 0:
        skill_overlap_score = len(matched_skills) / len(jd_skills)
    elif len(resume_skills) > 0:
        skill_overlap_score = 0.5
    else:
        skill_overlap_score = 0.0

    keyword_density = calculate_keyword_density(resume_text, list(jd_skills))

    return {
        "tfidf_score": tfidf_score,
        "skill_overlap_score": float(skill_overlap_score),
        "keyword_density": float(keyword_density),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "extracted_skills": list(resume_skills),
        "jd_skills": list(jd_skills),
    }

def calculate_final_score(analysis_result, resume_text):
    
    tfidf   = analysis_result['tfidf_score']
    overlap = analysis_result['skill_overlap_score']
    kw_qual = analysis_result['keyword_density']

    base = (tfidf * 0.60) + (overlap * 0.25) + (kw_qual * 0.15)
    score = base * 100  

    edu_bonus = detect_education_level(resume_text)
    score += edu_bonus

    exp_bonus = detect_experience_years(resume_text)
    score += exp_bonus

    jd_skills = analysis_result['jd_skills']
    missing_skills = analysis_result['missing_skills']
    if len(jd_skills) > 0 and len(missing_skills) / len(jd_skills) > 0.5:
        penalty = ((len(missing_skills) / len(jd_skills)) - 0.5) * 10
        score -= penalty

    if len(resume_text) < 200:
        score *= 0.5

    return round(min(max(score, 0), 100), 2)

def get_recommendation(score):
    if score >= 75:
        return "Strong match – shortlist"
    elif score >= 50:
        return "Moderate match – review manually"
    else:
        return "Low match – not recommended"

def get_ai_summary(matched_skills, missing_skills, score, candidate_name="This candidate"):
    top_matched = ', '.join(matched_skills[:3]) if matched_skills else 'general skills'
    top_missing = ', '.join(missing_skills[:2]) if missing_skills else 'none'
    name = candidate_name if candidate_name != 'N/A' else 'This candidate'

    if score >= 75:
        return (f"{name} is an excellent match. Strong alignment with core requirements "
                f"including {top_matched}. Recommended for immediate interview.")
    elif score >= 50:
        return (f"{name} shows good potential. Meets key requirements ({top_matched}) "
                f"but may lack {top_missing}. Recommend a detailed review.")
    else:
        return (f"{name} does not strongly align with the role requirements. "
                f"Missing key skills such as {top_missing}.")

def process_all_resumes(resume_files, jd_text):
    
    results = []

    for file in resume_files:
        file.seek(0)
        raw_text = extract_text_from_pdf(file)

        candidate_info = extract_candidate_info(raw_text)

        analysis = analyze_resume(raw_text, jd_text)

        final_score = calculate_final_score(analysis, raw_text)

        highlighted = highlight_jd_keywords(raw_text, analysis['jd_skills'])

        results.append({
            "File Name":        file.name,
            "Candidate Name":   candidate_info['name'],
            "Email":            candidate_info['email'],
            "Phone":            candidate_info['phone'],
            "Match Score":      final_score,
            "Recommendation":   get_recommendation(final_score),
            "Matched Skills":   analysis["matched_skills"],
            "Missing Skills":   analysis["missing_skills"],
            "Extracted Skills": analysis["extracted_skills"],
            "JD Skills":        analysis["jd_skills"],
            "AI Summary":       get_ai_summary(
                                    analysis["matched_skills"],
                                    analysis["missing_skills"],
                                    final_score,
                                    candidate_info['name']
                                ),
            "Highlighted Text": highlighted,
            "Raw Text Length":  len(raw_text),
        })

    results.sort(key=lambda x: x["Match Score"], reverse=True)

    for idx, res in enumerate(results):
        res["Rank"] = idx + 1

    return results
