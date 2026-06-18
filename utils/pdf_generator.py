from fpdf import FPDF
import pandas as pd
from datetime import datetime

def _safe(text):
    
    if text is None:
        return ""
    text = str(text)
    for src, dst in [
        ("\u2014", "-"), ("\u2013", "-"),
        ("\u2018", "'"), ("\u2019", "'"),
        ("\u201c", '"'), ("\u201d", '"'),
        ("\u2026", "..."), ("\u2265", ">="),
        ("\u2264", "<="), ("\u2022", "-"),
        ("\u00b7", "*"),
    ]:
        text = text.replace(src, dst)
    return text.encode("latin-1", errors="replace").decode("latin-1")

def _join_list(lst, limit=None):
    if not isinstance(lst, list):
        return _safe(str(lst)) if lst else "None"
    items = lst[:limit] if limit else lst
    return _safe(", ".join(items)) if items else "None"

def _text_lines(pdf, w, text):
    
    words = text.split()
    lines = 1
    current_w = 0
    for word in words:
        word_w = pdf.get_string_width(word + " ")
        if current_w + word_w > w:
            lines += 1
            current_w = word_w
        else:
            current_w += word_w
    return lines

NAVY    = (15,  23,  42)
BLUE    = (59,  130, 246)
INDIGO  = (79,  70,  229)
GREEN   = (5,   150, 105)
AMBER   = (217, 119, 6)
RED     = (220, 38,  38)
GOLD    = (202, 138, 4)
SILVER  = (100, 116, 139)
BRONZE  = (154, 52,  18)
WHITE   = (255, 255, 255)
LIGHT   = (248, 250, 252)
BGRAY   = (241, 245, 249)
BORDER  = (203, 213, 225)
MUTED   = (100, 116, 139)
DARK    = (30,  41,  59)

def _score_color(score):
    if score >= 75: return GREEN
    if score >= 50: return AMBER
    return RED

def _medal_color(rank):
    return {1: GOLD, 2: SILVER, 3: BRONZE}.get(rank, MUTED)

def _medal_label(rank):
    return {1: "GOLD", 2: "SILVER", 3: "BRONZE"}.get(rank, f"#{rank}")

class CareerRankPDF(FPDF):

    def __init__(self, report_date=""):
        super().__init__()
        self.report_date = report_date
        self.cover_page = 1

    def header(self):
        if self.page_no() == self.cover_page:
            return                          

        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 13, style="F")

        self.set_font("helvetica", "B", 8)
        self.set_text_color(*BLUE)
        self.set_xy(10, 4)
        self.cell(80, 5, "CareerRank AI", new_x="RIGHT", new_y="LAST")

        self.set_font("helvetica", "", 7)
        self.set_text_color(180, 190, 200)
        self.cell(60, 5, "Recruitment Analysis Report", new_x="RIGHT", new_y="LAST")

        self.set_x(150)
        self.set_text_color(*WHITE)
        self.cell(50, 5, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")

        self.set_text_color(0, 0, 0)
        self.set_y(20)

    def footer(self):
        if self.page_no() == self.cover_page:
            return

        self.set_y(-14)
        self.set_draw_color(*BLUE)
        self.set_line_width(0.25)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_font("helvetica", "I", 7)
        self.set_text_color(*MUTED)
        self.cell(
            0, 5,
            f"Generated: {self.report_date}  |  CareerRank AI - Intelligent Candidate Screening  |  Confidential",
            align="C"
        )
        self.set_text_color(0, 0, 0)

    def filled_rect(self, x, y, w, h, color):
        self.set_fill_color(*color)
        self.rect(x, y, w, h, style="F")

    def bordered_rect(self, x, y, w, h, fill, border, lw=0.25):
        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(lw)
        self.rect(x, y, w, h, style="FD")

    def score_bar(self, x, y, w, h, score, color):
        
        self.set_fill_color(*BGRAY)
        self.rect(x, y, w, h, style="F")
        
        fill_w = max(2, (score / 100) * w)
        self.set_fill_color(*color)
        self.rect(x, y, fill_w, h, style="F")
        
        self.set_font("helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(x + 2, y + (h - 4) / 2)
        self.cell(fill_w - 2, 4, f"{score:.1f}%", new_x="RIGHT", new_y="LAST")
        self.set_text_color(0, 0, 0)

    def pill_badge(self, x, y, text, color):
        
        sw = self.get_string_width(text)
        bw = sw + 5
        self.set_fill_color(*color)
        self.rect(x, y, bw, 4.5, style="F")
        self.set_font("helvetica", "B", 6.5)
        self.set_text_color(*WHITE)
        self.set_xy(x + 1.5, y + 0.5)
        self.cell(sw + 2, 3.5, text, new_x="RIGHT", new_y="LAST")
        self.set_text_color(0, 0, 0)
        return bw + 1.5   

    def stat_box(self, x, y, w, h, label, value, sub, accent):
        
        self.bordered_rect(x, y, w, h, LIGHT, BORDER, 0.3)
        
        self.filled_rect(x, y, w, 2.5, accent)
        
        self.set_font("helvetica", "", 7)
        self.set_text_color(*MUTED)
        self.set_xy(x + 3, y + 5)
        self.cell(w - 6, 4, _safe(label.upper()), new_x="LMARGIN", new_y="NEXT")
        
        self.set_font("helvetica", "B", 16)
        self.set_text_color(*DARK)
        self.set_xy(x + 3, y + 10)
        self.cell(w - 6, 9, _safe(str(value)), new_x="LMARGIN", new_y="NEXT")
        
        self.set_font("helvetica", "", 7)
        self.set_text_color(*accent)
        self.set_xy(x + 3, y + 20)
        self.cell(w - 6, 4, _safe(sub), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)

    def section_title(self, text, icon=""):
        
        y = self.get_y()
        
        self.filled_rect(10, y, 3, 8, BLUE)
        
        self.set_font("helvetica", "B", 12)
        self.set_text_color(*NAVY)
        self.set_xy(16, y + 0.5)
        self.cell(0, 7, _safe(f"{icon}  {text}" if icon else text), new_x="LMARGIN", new_y="NEXT")
        
        self.set_draw_color(*BORDER)
        self.set_line_width(0.25)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
        self.set_text_color(0, 0, 0)

    def body_text(self, text, color=None):
        color = color or DARK
        self.set_font("helvetica", "", 9.5)
        self.set_text_color(*color)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.5, _safe(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def kv_pair(self, key, value):
        self.set_x(self.l_margin)
        self.set_font("helvetica", "B", 9)
        self.set_text_color(*NAVY)
        self.cell(58, 6, _safe(key) + ":", new_x="RIGHT", new_y="LAST")
        self.set_font("helvetica", "", 9)
        self.set_text_color(*DARK)
        self.set_x(self.l_margin + 58)
        self.multi_cell(0, 6, _safe(str(value)), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)

def _draw_cover(pdf, total, avg, top_name, top_score, shortlisted):
    
    pdf.filled_rect(0, 0, 210, 110, NAVY)

    pdf.set_fill_color(*BLUE)
    pdf.set_draw_color(*BLUE)
    
    pdf.filled_rect(155, -20, 70, 70, INDIGO)
    
    pdf.filled_rect(155, 50, 70, 20, NAVY)

    for size, col in [(22, BLUE), (15, NAVY), (9, BLUE), (4, WHITE)]:
        half = size // 2
        pdf.set_fill_color(*col)
        
        pdf.rect(105 - half, 22 - half + 5, size, size, style="F")

    pdf.set_font("helvetica", "B", 28)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(10, 48)
    pdf.cell(0, 14, "CareerRank AI", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(147, 197, 253)   
    pdf.set_xy(10, 66)
    pdf.cell(0, 7, "Recruitment Analysis Report", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("helvetica", "", 8)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(10, 78)
    pdf.cell(0, 5, f"Generated on {pdf.report_date}", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.5)
    pdf.line(40, 87, 170, 87)

    pdf.set_font("helvetica", "I", 9)
    pdf.set_text_color(203, 213, 225)
    pdf.set_xy(10, 90)
    pdf.cell(0, 5, "Rank the right talent with AI in seconds.", align="C", new_x="LMARGIN", new_y="NEXT")

    bx, by, bw, bh, gap = 12, 118, 43, 36, 4
    stats = [
        ("Total Resumes", str(total), "Analysed", BLUE),
        ("Avg Match Score", f"{avg:.1f}%", "Across all", INDIGO),
        ("Shortlisted", str(shortlisted), "Score >= 75%", GREEN),
        ("Top Score", f"{top_score}%", _safe(top_name[:16] + ("..." if len(top_name) > 16 else "")), GOLD),
    ]
    for i, (label, value, sub, accent) in enumerate(stats):
        pdf.stat_box(bx + i * (bw + gap), by, bw, bh, label, value, sub, accent)

    pdf.set_font("helvetica", "B", 8)
    pdf.set_text_color(*NAVY)
    pdf.set_xy(10, 162)
    pdf.cell(0, 5, "REPORT CONTENTS", align="C", new_x="LMARGIN", new_y="NEXT")

    contents = [
        ("01", "Abstract & Introduction"),
        ("02", "Tools & Processing Methodology"),
        ("03", "Summary Metrics"),
        ("04", "Ranked Candidates"),
        ("05", "Conclusion"),
    ]
    for num, title in contents:
        cx = 55
        cy = pdf.get_y() + 2
        
        pdf.filled_rect(cx - 2, cy, 10, 6, BLUE)
        pdf.set_font("helvetica", "B", 7)
        pdf.set_text_color(*WHITE)
        pdf.set_xy(cx - 1, cy + 0.8)
        pdf.cell(8, 4.5, num, new_x="RIGHT", new_y="LAST")
        
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(*DARK)
        pdf.set_xy(cx + 10, cy + 0.6)
        pdf.cell(100, 5, title, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_draw_color(*BORDER)
        pdf.dashed_line(cx + 10, cy + 5.5, 155, cy + 5.5, dash_length=1, space_length=1)

    pdf.set_text_color(0, 0, 0)

def _draw_candidate_card(pdf, row, rank):
    score       = row["Match Score"]
    bar_color   = _score_color(score)
    medal_color = _medal_color(rank)
    name        = _safe(row.get("Candidate Name") or row["File Name"])
    email       = _safe(row.get("Email", "N/A"))
    phone       = _safe(row.get("Phone", "N/A"))
    rec         = _safe(row.get("Recommendation", ""))
    ai_sum      = _safe(row.get("AI Summary", ""))
    matched     = _join_list(row.get("Matched Skills", []))
    missing     = _join_list(row.get("Missing Skills", []), 6)

    cw = 190
    text_w = cw - 42

    pdf.set_font("helvetica", "", 8.5)
    matched_lines = _text_lines(pdf, text_w, matched)
    missing_lines = _text_lines(pdf, text_w, missing)
    pdf.set_font("helvetica", "I", 8.5)
    ai_lines      = _text_lines(pdf, text_w, ai_sum)
    
    card_h = 32 + (matched_lines * 5) + (missing_lines * 5) + (ai_lines * 5) + 12

    if pdf.get_y() + card_h > 275:
        pdf.add_page()

    cx, cy = pdf.l_margin, pdf.get_y()

    pdf.bordered_rect(cx, cy, cw, card_h, LIGHT, BORDER, 0.2)

    pdf.filled_rect(cx, cy, 3, card_h, medal_color)

    pdf.set_font("helvetica", "B", 8)
    pdf.set_text_color(*WHITE)
    pdf.filled_rect(cx + 6, cy + 6, 18, 6, medal_color)
    pdf.set_xy(cx + 6, cy + 6.5)
    pdf.cell(18, 5, _medal_label(rank), align="C", new_x="RIGHT", new_y="LAST")

    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.set_xy(cx + 28, cy + 5.5)
    pdf.cell(120, 6, name, new_x="RIGHT", new_y="LAST")

    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(*bar_color)
    pdf.set_xy(cx + cw - 38, cy + 4)
    pdf.cell(32, 8, f"{score:.1f}%", align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("helvetica", "", 8.5)
    pdf.set_text_color(*MUTED)
    pdf.set_xy(cx + 28, cy + 11.5)
    pdf.cell(100, 5, f"{email}   |   {phone}", new_x="LMARGIN", new_y="NEXT")

    bar_y = cy + 13
    pdf.score_bar(cx + cw - 36, bar_y, 30, 4, score, bar_color)

    rec_color = _score_color(score)
    pdf.pill_badge(cx + 6, cy + 20, rec.upper()[:35], rec_color)

    div_y = cy + 28
    pdf.set_draw_color(*BORDER)
    pdf.set_line_width(0.2)
    pdf.line(cx + 6, div_y, cx + cw - 6, div_y)

    text_y = div_y + 4

    pdf.set_font("helvetica", "B", 8.5)
    pdf.set_text_color(*DARK)
    pdf.set_xy(cx + 6, text_y)
    pdf.cell(30, 5, "Matched Skills:", new_x="RIGHT", new_y="LAST")
    
    pdf.set_font("helvetica", "", 8.5)
    pdf.set_text_color(*GREEN)
    pdf.set_x(cx + 36)
    pdf.multi_cell(text_w, 5, matched, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("helvetica", "B", 8.5)
    pdf.set_text_color(*DARK)
    pdf.set_xy(cx + 6, pdf.get_y())
    pdf.cell(30, 5, "Missing Skills:", new_x="RIGHT", new_y="LAST")
    
    pdf.set_font("helvetica", "", 8.5)
    pdf.set_text_color(*RED)
    pdf.set_x(cx + 36)
    pdf.multi_cell(text_w, 5, missing, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(1)

    pdf.set_font("helvetica", "B", 8.5)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(cx + 6, pdf.get_y())
    pdf.cell(30, 5, "AI Insight:", new_x="RIGHT", new_y="LAST")
    
    pdf.set_font("helvetica", "I", 8.5)
    pdf.set_text_color(*DARK)
    pdf.set_x(cx + 36)
    pdf.multi_cell(text_w, 5, ai_sum, new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(cy + card_h + 6)
    pdf.set_text_color(0, 0, 0)

def generate_pdf_report(results_df, total_resumes, top_candidate, avg_score):
    
    report_date = datetime.now().strftime("%d %b %Y, %I:%M %p")
    shortlisted = len(results_df[results_df["Match Score"] >= 75])

    top_name  = "N/A"
    top_score = 0
    if top_candidate:
        top_name  = top_candidate.get("Candidate Name") or top_candidate.get("File Name", "N/A")
        top_score = top_candidate.get("Match Score", 0)

    pdf = CareerRankPDF(report_date=report_date)
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.add_page()
    _draw_cover(pdf, total_resumes, avg_score, top_name, top_score, shortlisted)

    pdf.add_page()

    pdf.section_title("01   Abstract & Introduction")
    pdf.body_text(
        "CareerRank AI is an intelligent recruitment screening platform built for modern HR teams. "
        "This report presents the automated analysis of candidate resumes against the provided "
        "Job Description (JD). Using a multi-weighted NLP scoring system comprising TF-IDF "
        "cosine similarity (60%), skill-overlap scoring (25%), and keyword match quality (15%), "
        "supplemented by education-level and experience-year bonuses, each candidate is assigned "
        "a match score out of 100. All results are ranked from highest to lowest suitability."
    )

    pdf.ln(3)
    pdf.section_title("02   Tools & Processing Methodology")

    tools = ["Python 3", "Streamlit", "spaCy", "NLTK", "scikit-learn",
             "pdfplumber", "Plotly", "WordCloud", "fpdf2"]
    pdf.set_x(pdf.l_margin)
    x_cursor = pdf.l_margin
    y_tools = pdf.get_y()
    for tool in tools:
        tw = pdf.get_string_width(tool) + 6
        if x_cursor + tw > 198:
            x_cursor = pdf.l_margin
            y_tools += 7
        pdf.pill_badge(x_cursor, y_tools, tool, INDIGO)
        x_cursor += tw + 3
    pdf.set_y(y_tools + 10)

    steps = [
        ("PDF Parsing",       "Extract raw text from each resume using pdfplumber."),
        ("Preprocessing",     "Lowercase, remove noise, lemmatise with spaCy / NLTK."),
        ("Candidate NER",     "Extract name, email, and phone via regex patterns."),
        ("Skill Extraction",  "Match against a curated 60+ skill knowledge base."),
        ("TF-IDF Vectors",    "Vectorise JD and resume text for cosine similarity."),
        ("Keyword Density",   "Measure JD keyword hit-rate per resume."),
        ("Bonus Detection",   "Detect education level and years of experience."),
        ("Final Scoring",     "Combine weights + bonuses - missing-skill penalty."),
        ("Ranking",           "Sort all candidates descending by final score."),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        sy = pdf.get_y()
        
        pdf.filled_rect(pdf.l_margin, sy + 0.5, 7, 6, BLUE)
        pdf.set_font("helvetica", "B", 7)
        pdf.set_text_color(*WHITE)
        pdf.set_xy(pdf.l_margin, sy + 1.3)
        pdf.cell(7, 4, str(i), align="C", new_x="RIGHT", new_y="LAST")
        
        pdf.set_font("helvetica", "B", 8.5)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(pdf.l_margin + 9, sy + 0.5)
        pdf.cell(38, 5, _safe(title), new_x="RIGHT", new_y="LAST")
        
        pdf.set_font("helvetica", "", 8.5)
        pdf.set_text_color(*DARK)
        pdf.set_x(pdf.l_margin + 48)
        pdf.multi_cell(0, 5, _safe(desc), new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.section_title("03   Summary Metrics")

    metrics = [
        ("Total Resumes", str(total_resumes), "Analysed",          BLUE),
        ("Avg Match Score", f"{avg_score:.2f}%", "Across all",      INDIGO),
        ("Shortlisted",   str(shortlisted),   "Score >= 75%",       GREEN),
        ("Top Score",     f"{top_score}%",    _safe(top_name[:18]), GOLD),
    ]
    bx, by, bw, bh, gap = 10, pdf.get_y(), 43, 36, 4
    for i, (lbl, val, sub, acc) in enumerate(metrics):
        pdf.stat_box(bx + i * (bw + gap), by, bw, bh, lbl, val, sub, acc)
    pdf.set_y(by + bh + 10)

    pdf.set_font("helvetica", "B", 9)
    pdf.set_text_color(*NAVY)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 6, "Scoring Formula:", new_x="LMARGIN", new_y="NEXT")

    fy = pdf.get_y()
    pdf.bordered_rect(pdf.l_margin, fy, 190, 30, BGRAY, BLUE, 0.4)
    formula_lines = [
        "Final Score = (TF-IDF Similarity x 0.60)",
        "            + (Skill Overlap Score x 0.25)",
        "            + (Keyword Density Score x 0.15)  x 100",
        "            + Education Bonus (0-5 pts) + Experience Bonus (0-5 pts)",
        "            - Missing Skill Penalty  |  Capped at 100",
    ]
    pdf.set_font("helvetica", "", 8)
    pdf.set_text_color(*DARK)
    for j, line in enumerate(formula_lines):
        pdf.set_xy(pdf.l_margin + 4, fy + 3 + j * 5)
        pdf.cell(0, 4.5, _safe(line), new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(fy + 36)

    pdf.set_font("helvetica", "B", 8.5)
    pdf.set_text_color(*DARK)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 6, "Score Interpretation:", new_x="LMARGIN", new_y="NEXT")

    legends = [
        ("75 - 100%", "Strong match   - Shortlist for interview",    GREEN),
        ("50 -  74%", "Moderate match - Manual review recommended",   AMBER),
        (" 0 -  49%", "Low match      - Not recommended",             RED),
    ]
    for ltext, ldesc, lcolor in legends:
        ly = pdf.get_y()
        pdf.filled_rect(pdf.l_margin, ly + 1, 3, 5, lcolor)
        pdf.set_font("helvetica", "B", 8.5)
        pdf.set_text_color(*lcolor)
        pdf.set_xy(pdf.l_margin + 6, ly)
        pdf.cell(28, 7, ltext, new_x="RIGHT", new_y="LAST")
        pdf.set_font("helvetica", "", 8.5)
        pdf.set_text_color(*DARK)
        pdf.cell(140, 7, _safe(ldesc), new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.section_title("04   Ranked Candidates")
    pdf.set_font("helvetica", "", 8)
    pdf.set_text_color(*MUTED)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 5, f"All {len(results_df)} candidate(s) ranked from highest to lowest AI match score.",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_text_color(0, 0, 0)

    for _, row in results_df.iterrows():
        _draw_candidate_card(pdf, row, int(row["Rank"]))

    pdf.add_page()
    pdf.section_title("05   Conclusion & Recommendations")
    pdf.body_text(
        "CareerRank AI has successfully ranked all submitted candidates using a robust, "
        "multi-factor NLP scoring pipeline. The automated process significantly reduces "
        "manual screening time while ensuring objective, data-driven shortlisting decisions."
    )
    pdf.body_text(
        "Human review of the top-ranked candidates is strongly recommended to evaluate "
        "cultural fit, communication skills, problem-solving ability, and other qualitative "
        "factors not captured in a resume. The AI score provides a reliable first filter, "
        "not a final verdict."
    )
    pdf.body_text(
        "For best results in future analyses: ensure resumes are machine-readable (not "
        "scanned images), use detailed Job Descriptions with explicit skill requirements, "
        "and upload a minimum of 5 candidate resumes per role for meaningful comparison."
    )

    pdf.ln(8)
    closing_y = pdf.get_y()
    pdf.bordered_rect(pdf.l_margin, closing_y, 190, 22, BGRAY, BLUE, 0.4)
    pdf.filled_rect(pdf.l_margin, closing_y, 190, 3, BLUE)
    pdf.set_font("helvetica", "B", 10)
    pdf.set_text_color(*NAVY)
    pdf.set_xy(pdf.l_margin + 5, closing_y + 7)
    pdf.cell(0, 6, "CareerRank AI  -  Intelligent Recruitment Screening Platform", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 8)
    pdf.set_text_color(*MUTED)
    pdf.set_xy(pdf.l_margin + 5, closing_y + 14)
    pdf.cell(0, 5, "Rank the right talent with AI in seconds.  |  Report generated automatically.", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)

    return bytes(pdf.output())
