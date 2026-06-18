import streamlit as st
import html as _html

def _e(val):
    
    return _html.escape(str(val) if val is not None else '')

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ════════════════════════════════════════════
           BASE
        ════════════════════════════════════════════ */
        html, body, .stApp {
            background-color: #0F172A !important;
            color: #F8FAFC;
            font-family: 'Inter', sans-serif;
        }

        /* ════════════════════════════════════════════
           GLASS CARD
        ════════════════════════════════════════════ */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.09);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
            padding: 24px;
            margin-bottom: 20px;
            transition: transform 0.25s ease, box-shadow 0.25s ease, border 0.25s ease;
            box-sizing: border-box;
        }
        .glass-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(59, 130, 246, 0.18);
            border: 1px solid rgba(59, 130, 246, 0.35);
        }

        /* ════════════════════════════════════════════
           GRADIENT TEXT
        ════════════════════════════════════════════ */
        .gradient-text {
            background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #10B981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
        }

        /* ════════════════════════════════════════════
           HERO SECTION
        ════════════════════════════════════════════ */
        .hero-section {
            text-align: center;
            padding: 60px 40px 40px;
            animation: fadeSlideIn 1.2s ease forwards;
        }
        .hero-title {
            font-size: clamp(2rem, 5vw, 3.2rem);
            margin: 0 0 10px;
            line-height: 1.2;
        }
        .hero-tagline {
            font-size: clamp(0.95rem, 2.5vw, 1.2rem);
            color: #CBD5E1;
            margin: 0 0 6px;
        }
        .hero-sub {
            font-size: clamp(0.78rem, 1.8vw, 0.9rem);
            color: #64748B;
        }
        @keyframes fadeSlideIn {
            0%  { opacity: 0; transform: translateY(30px); }
            100%{ opacity: 1; transform: translateY(0); }
        }

        /* ════════════════════════════════════════════
           HOW IT WORKS — CSS GRID (responsive)
        ════════════════════════════════════════════ */
        .steps-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 20px 0 10px;
        }
        .step-card {
            background: rgba(59,130,246,0.07);
            border: 1px solid rgba(59,130,246,0.18);
            border-radius: 14px;
            padding: 24px 18px;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            box-sizing: border-box;
        }
        .step-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(59,130,246,0.2);
        }
        .step-number {
            width: 44px; height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg,#3B82F6,#8B5CF6);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.1rem; font-weight: 700;
            margin: 0 auto 14px;
            color: white;
        }
        .step-title {
            margin: 0 0 8px;
            font-size: clamp(0.85rem, 1.5vw, 0.95rem);
            color: #F8FAFC;
            font-weight: 600;
        }
        .step-desc {
            margin: 0;
            font-size: clamp(0.75rem, 1.2vw, 0.82rem);
            color: #94A3B8;
            line-height: 1.6;
        }

        /* ════════════════════════════════════════════
           METRICS GRID — CSS GRID (responsive)
        ════════════════════════════════════════════ */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.09);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
            padding: 18px 14px;
            text-align: center;
            transition: transform 0.25s, box-shadow 0.25s, border 0.25s;
            box-sizing: border-box;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 28px rgba(59,130,246,0.15);
            border-color: rgba(59,130,246,0.35);
        }
        .metric-label {
            font-size: clamp(0.7rem, 1.2vw, 0.8rem);
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin: 0 0 6px;
        }
        .metric-value {
            font-size: clamp(1.5rem, 3vw, 2rem);
            font-weight: 700;
            color: #F8FAFC;
            margin: 0 0 4px;
            word-break: break-word;
        }
        .metric-sub {
            font-size: clamp(0.7rem, 1.2vw, 0.8rem);
            color: #3B82F6;
            margin: 0;
        }

        /* ════════════════════════════════════════════
           TOP 3 SPOTLIGHT — CSS GRID (responsive)
        ════════════════════════════════════════════ */
        .spotlight-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }
        .spotlight-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 24px 18px;
            text-align: center;
            box-sizing: border-box;
            transition: transform 0.2s;
        }
        .spotlight-card:hover { transform: translateY(-3px); }
        .spotlight-gold   { border: 2px solid #F59E0B; box-shadow: 0 0 24px rgba(245,158,11,0.25); }
        .spotlight-silver { border: 2px solid #94A3B8; box-shadow: 0 0 24px rgba(148,163,184,0.2); }
        .spotlight-bronze { border: 2px solid #CD7F32; box-shadow: 0 0 24px rgba(205,127,50,0.2); }
        .spotlight-medal  { font-size: 2.4rem; margin-bottom: 8px; }
        .spotlight-name   { font-size: clamp(0.88rem, 1.8vw, 1rem); font-weight: 700; margin: 0 0 4px; }
        .spotlight-file   { font-size: clamp(0.7rem, 1.2vw, 0.75rem); color: #64748B; margin: 0 0 10px; }
        .spotlight-score  { font-size: clamp(1.6rem, 3.5vw, 2rem); font-weight: 800; }
        .spotlight-divider{ border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 12px 0; }
        .spotlight-stats  { font-size: clamp(0.7rem, 1.2vw, 0.75rem); color: #94A3B8; margin: 0; }

        /* ════════════════════════════════════════════
           BADGES
        ════════════════════════════════════════════ */
        .badge {
            padding: 3px 9px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            margin: 2px 3px;
            white-space: nowrap;
        }
        .badge-success { background: rgba(16,185,129,0.15); color:#10B981; border:1px solid rgba(16,185,129,0.35); }
        .badge-warning { background: rgba(245,158,11,0.15); color:#F59E0B; border:1px solid rgba(245,158,11,0.35); }
        .badge-danger  { background: rgba(239,68,68,0.15);  color:#EF4444; border:1px solid rgba(239,68,68,0.35); }
        .badge-info    { background: rgba(59,130,246,0.15); color:#3B82F6; border:1px solid rgba(59,130,246,0.35); }

        /* ════════════════════════════════════════════
           CANDIDATE CARD HEADER (responsive flex)
        ════════════════════════════════════════════ */
        .cand-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 10px;
        }
        .cand-info { flex: 1 1 180px; min-width: 0; }
        .cand-score { text-align: right; flex-shrink: 0; }
        .cand-name {
            margin: 0 0 4px;
            color: #F8FAFC;
            font-size: clamp(0.9rem, 2vw, 1.05rem);
            font-weight: 700;
            word-break: break-word;
        }
        .cand-filename { margin: 0 0 2px; font-size: 0.78rem; color: #64748B; word-break: break-all; }
        .meta-row { font-size: 0.8rem; color: #94A3B8; margin: 4px 0; word-break: break-all; }
        .meta-row span { color: #CBD5E1; font-weight: 500; }
        .cand-score-val { font-size: clamp(1.5rem, 3.5vw, 1.8rem); font-weight: 800; }

        /* ════════════════════════════════════════════
           KEYWORD HIGHLIGHT PREVIEW
        ════════════════════════════════════════════ */
        .kw-preview {
            background: rgba(0,0,0,0.25);
            border-radius: 10px;
            padding: 14px;
            font-size: 0.82rem;
            line-height: 1.7;
            color: #CBD5E1;
            max-height: 220px;
            overflow-y: auto;
            word-break: break-word;
        }

        /* ════════════════════════════════════════════
           SECTION LABELS
        ════════════════════════════════════════════ */
        .section-label {
            font-size: 0.75rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 0 0 4px;
        }

        /* ════════════════════════════════════════════
           BUTTONS
        ════════════════════════════════════════════ */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #3B82F6, #6366F1);
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
            transition: all 0.3s;
            width: 100%;
        }
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #2563EB, #4F46E5);
            box-shadow: 0 0 18px rgba(59,130,246,0.5);
            transform: scale(1.02);
        }

        /* ════════════════════════════════════════════
           STREAMLIT COLUMN RESPONSIVE STACKING
        ════════════════════════════════════════════ */

        /* Tablet (≤ 1024px): 4-col metrics → 2×2 handled by CSS Grid */

        /* Mobile (≤ 768px): Stack ALL Streamlit columns */
        @media screen and (max-width: 768px) {

            /* Stack st.columns */
            [data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
                gap: 0 !important;
            }
            [data-testid="stHorizontalBlock"] > [data-testid="column"] {
                width: 100% !important;
                flex: 0 0 100% !important;
                min-width: 100% !important;
            }

            /* Hero */
            .hero-section { padding: 30px 14px 22px !important; }

            /* Glass cards */
            .glass-card {
                padding: 16px !important;
                border-radius: 12px !important;
                margin-bottom: 14px !important;
            }
            .glass-card:hover { transform: none !important; }

            /* Step cards */
            .step-card { padding: 16px 12px !important; }
            .step-card:hover { transform: none !important; }

            /* Metric cards */
            .metric-card:hover { transform: none !important; }

            /* Spotlight */
            .spotlight-card:hover { transform: none !important; }

            /* Badges wrap */
            .badge { font-size: 0.7rem; margin: 2px 2px; }

            /* File uploader */
            [data-testid="stFileUploader"] { width: 100% !important; }

            /* Slider */
            [data-testid="stSlider"] { width: 100% !important; }

            /* Plotly charts */
            .js-plotly-plot .plot-container { width: 100% !important; }

            /* Download buttons */
            [data-testid="stDownloadButton"] button { width: 100% !important; }

            /* Input section heading */
            h3 { font-size: 1rem !important; }

            /* Text area */
            textarea { font-size: 0.9rem !important; }
        }

        /* Extra small mobile (≤ 480px) */
        @media screen and (max-width: 480px) {
            .hero-section { padding: 22px 10px 18px !important; }
            .glass-card { padding: 12px !important; }
            .badge { font-size: 0.65rem; padding: 2px 5px; }
            .step-number { width: 36px; height: 36px; font-size: 0.95rem; }
            .steps-grid { gap: 10px; }
            .metrics-grid { gap: 10px; }
            .spotlight-grid { gap: 10px; }
        }

        /* ════════════════════════════════════════════
           HIDE STREAMLIT CHROME
        ════════════════════════════════════════════ */
        #MainMenu { visibility: hidden; }
        footer     { visibility: hidden; }
        header     { visibility: hidden; }

        /* ════════════════════════════════════════════
        /* ════════════════════════════════════════════
           SECTION HEADER
        ════════════════════════════════════════════ */
        .section-header {
            text-align: center;
            margin: 10px 0 24px;
        }
        .section-header h2 {
            font-size: clamp(1.2rem, 3vw, 1.6rem);
            font-weight: 700;
            color: #F8FAFC;
            margin: 0 0 6px;
        }
        .section-header p {
            font-size: clamp(0.78rem, 1.5vw, 0.88rem);
            color: #64748B;
            margin: 0;
        }

        /* ════════════════════════════════════════════
           INPUT SECTION LABELS
        ════════════════════════════════════════════ */
        .input-section-label {
            font-size: 0.92rem;
            font-weight: 600;
            color: #CBD5E1;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .input-icon { font-size: 1.1rem; }

        /* Glass effect for input columns */
        [data-testid="column"] {
            background: rgba(255,255,255,0.03);
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.07);
            padding: 20px 18px !important;
            transition: border 0.25s;
        }
        [data-testid="column"]:focus-within {
            border-color: rgba(59,130,246,0.35);
        }

        /* Uploaded file chip */
        .file-chip {
            margin: 4px 0;
            font-size: 0.8rem;
            color: #64748B;
            word-break: break-all;
            padding: 4px 10px;
            background: rgba(59,130,246,0.07);
            border-radius: 8px;
            border: 1px solid rgba(59,130,246,0.15);
        }

        /* ════════════════════════════════════════════
           CARD TITLE (sub-section labels)
        ════════════════════════════════════════════ */
        .card-title {
            font-size: clamp(0.88rem, 1.8vw, 1rem);
            font-weight: 700;
            color: #F8FAFC;
            margin: 0 0 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.07);
        }

        /* ════════════════════════════════════════════
           DIVIDER
        ════════════════════════════════════════════ */
        .section-divider {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.07);
            margin: 32px 0;
        }
        .section-divider-lg {
            border: none;
            border-top: 1px solid rgba(59,130,246,0.2);
            margin: 48px 0 36px;
        }

        /* ════════════════════════════════════════════
           STREAMLIT WIDGET OVERRIDES
        ════════════════════════════════════════════ */
        .stTextArea textarea {
            background-color: rgba(255,255,255,0.04) !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 10px !important;
        }
        [data-testid="stSlider"] [data-testid="stSliderThumb"] {
            background: #3B82F6 !important;
        }
        details summary {
            color: #94A3B8 !important;
            font-size: 0.87rem !important;
        }
        /* File uploader styling */
        [data-testid="stFileUploader"] {
            width: 100%;
        }
        [data-testid="stFileUploader"] section {
            border: 1px dashed rgba(59,130,246,0.35) !important;
            border-radius: 10px !important;
            background: rgba(59,130,246,0.04) !important;
        }
        /* Download buttons */
        [data-testid="stDownloadButton"] button {
            background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(99,102,241,0.15)) !important;
            border: 1px solid rgba(59,130,246,0.35) !important;
            color: #93C5FD !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.25s !important;
        }
        [data-testid="stDownloadButton"] button:hover {
            background: linear-gradient(135deg, rgba(59,130,246,0.3), rgba(99,102,241,0.3)) !important;
            border-color: rgba(59,130,246,0.6) !important;
            transform: translateY(-2px);
        }
        /* Success message */
        [data-testid="stAlert"] {
            border-radius: 10px !important;
        }
        /* Score slider */
        [data-testid="stSlider"] {
            padding: 0 4px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_hero():
    st.markdown("""
        <div class="hero-section glass-card">
            <div style="font-size:clamp(2.5rem,6vw,3.5rem);margin-bottom:4px;">🎯</div>
            <h1 class="hero-title">
                <span class="gradient-text">CareerRank AI</span>
            </h1>
            <p class="hero-tagline">Rank the right talent with AI in seconds.</p>
            <p class="hero-sub">Intelligent Resume Ranking &amp; Candidate Screening Platform</p>
        </div>
    """, unsafe_allow_html=True)

def render_how_it_works():
    st.markdown("""
        <h3 style='text-align:center;margin:10px 0 20px;color:#94A3B8;
                   font-size:0.85rem;letter-spacing:0.12em;text-transform:uppercase;'>
            How It Works
        </h3>
        <div class="steps-grid">
            <div class="step-card">
                <div class="step-number">1</div>
                <div style="font-size:1.6rem;margin-bottom:10px;">📝</div>
                <h4 class="step-title">Paste Job Description</h4>
                <p class="step-desc">Enter the full JD with required skills, experience, and responsibilities.</p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <div style="font-size:1.6rem;margin-bottom:10px;">📤</div>
                <h4 class="step-title">Upload Resumes</h4>
                <p class="step-desc">Upload one or more candidate PDF resumes in bulk for analysis.</p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <div style="font-size:1.6rem;margin-bottom:10px;">🤖</div>
                <h4 class="step-title">AI Analysis</h4>
                <p class="step-desc">NLP engine extracts skills, calculates TF-IDF similarity, keyword density, and scores every resume.</p>
            </div>
            <div class="step-card">
                <div class="step-number">4</div>
                <div style="font-size:1.6rem;margin-bottom:10px;">🏆</div>
                <h4 class="step-title">Ranked Results</h4>
                <p class="step-desc">Ranked leaderboard with AI insights, skill tags, and downloadable reports.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_section_header(title, subtitle=""):
    subtitle_html = f"<p>{_e(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f'<div class="section-header"><h2>{_e(title)}</h2>{subtitle_html}</div>',
        unsafe_allow_html=True
    )

def render_divider(large=False):
    cls = "section-divider-lg" if large else "section-divider"
    st.markdown(f'<hr class="{cls}">', unsafe_allow_html=True)

def render_metrics_row(total, avg_score, top_name, top_score, shortlisted):
    
    top_score_str = f"{top_score}% match" if top_score else ""
    top_name_display = (top_name[:18] + "…") if top_name and len(top_name) > 20 else (top_name or "N/A")
    st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <p class="metric-label">Total Analysed</p>
                <div class="metric-value">{total}</div>
                <p class="metric-sub">Resumes</p>
            </div>
            <div class="metric-card">
                <p class="metric-label">Avg Match Score</p>
                <div class="metric-value">{avg_score:.1f}%</div>
                <p class="metric-sub">Across all resumes</p>
            </div>
            <div class="metric-card">
                <p class="metric-label">Top Candidate</p>
                <div class="metric-value" style="font-size:clamp(1rem,2.5vw,1.4rem);">
                    {top_name_display}
                </div>
                <p class="metric-sub">{top_score_str}</p>
            </div>
            <div class="metric-card">
                <p class="metric-label">Shortlisted</p>
                <div class="metric-value">{shortlisted}</div>
                <p class="metric-sub">Score ≥ 75%</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, subtitle=""):
    st.markdown(f"""
        <div class="metric-card" style="margin-bottom:16px;">
            <p class="metric-label">{title}</p>
            <div class="metric-value">{value}</div>
            <p class="metric-sub">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

def render_top3_spotlight(results):
    
    st.markdown("""
        <h2 style='text-align:center;margin:40px 0 6px;font-size:clamp(1.3rem,3vw,1.8rem);'>
            <span class='gradient-text'>&#127942; Top 3 Candidates</span>
        </h2>
        <p style='text-align:center;color:#64748B;font-size:clamp(0.78rem,1.5vw,0.85rem);margin-bottom:20px;'>
            Highest-ranked candidates based on AI scoring
        </p>
    """, unsafe_allow_html=True)

    medals = [
        ("&#129351;", "spotlight-gold",   "#F59E0B"),
        ("&#129352;", "spotlight-silver", "#94A3B8"),
        ("&#129353;", "spotlight-bronze", "#CD7F32"),
    ]

    top = results[:3]
    cards_html = ""
    for cand, (medal, cls, color) in zip(top, medals):
        score     = cand['Match Score']
        badge_cls = "badge-success" if score >= 75 else "badge-warning" if score >= 50 else "badge-danger"
        
        rec     = _e(cand['Recommendation'])
        name    = _e(cand.get('Candidate Name', 'N/A'))
        fname   = _e(cand['File Name'])
        matched = len(cand.get('Matched Skills', []))
        missing = len(cand.get('Missing Skills', []))
        cards_html += (
            f'<div class="spotlight-card {cls}">'
            f'<div class="spotlight-medal">{medal}</div>'
            f'<div class="spotlight-name" style="color:{color};">{name}</div>'
            f'<div class="spotlight-file">{fname}</div>'
            f'<div class="spotlight-score" style="color:{color};">{score}%</div>'
            f'<span class="badge {badge_cls}" style="margin-top:8px;display:inline-block;">{rec}</span>'
            f'<hr class="spotlight-divider">'
            f'<p class="spotlight-stats">&#10003; {matched} matched &nbsp;|&nbsp; {missing} missing</p>'
            f'</div>'
        )

    st.markdown(f'<div class="spotlight-grid">{cards_html}</div>', unsafe_allow_html=True)

def render_candidate_card(candidate):
    score       = candidate['Match Score']
    score_color = '#10B981' if score >= 75 else '#F59E0B' if score >= 50 else '#EF4444'
    badge_cls   = "badge-success" if score >= 75 else "badge-warning" if score >= 50 else "badge-danger"

    matched_html = "".join(
        f"<span class='badge badge-success'>{_e(s)}</span>"
        for s in candidate.get('Matched Skills', [])
    ) or "<span class='badge badge-info'>None detected</span>"

    missing_html = "".join(
        f"<span class='badge badge-danger'>{_e(s)}</span>"
        for s in candidate.get('Missing Skills', [])[:6]
    ) or "<span class='badge badge-info'>None</span>"

    name      = _e(candidate.get('Candidate Name', 'N/A'))
    email     = _e(candidate.get('Email', 'N/A'))
    phone     = _e(candidate.get('Phone', 'N/A'))
    fname     = _e(candidate.get('File Name', ''))
    rank      = _e(candidate.get('Rank', ''))
    rec       = _e(candidate.get('Recommendation', ''))
    ai_sum    = _e(candidate.get('AI Summary', ''))

    st.markdown(
        f'<div class="glass-card">'
        f'<div class="cand-header">'
        f'<div class="cand-info">'
        f'<h3 class="cand-name">#{rank} &mdash; {name}</h3>'
        f'<p class="cand-filename">{fname}</p>'
        f'<div class="meta-row">&#128231; <span>{email}</span></div>'
        f'<div class="meta-row">&#128222; <span>{phone}</span></div>'
        f'</div>'
        f'<div class="cand-score">'
        f'<div class="cand-score-val" style="color:{score_color};">{score}%</div>'
        f'<span class="badge {badge_cls}">{rec}</span>'
        f'</div>'
        f'</div>'
        f'<hr style="border-color:rgba(255,255,255,0.07);margin:14px 0;">'
        f'<p style="margin:0 0 12px;font-size:clamp(0.8rem,1.5vw,0.85rem);color:#CBD5E1;line-height:1.6;">'
        f'<strong style="color:#3B82F6;">&#129302; AI Insight:</strong> {ai_sum}'
        f'</p>'
        f'<div style="margin-bottom:10px;">'
        f'<p class="section-label">Matched Skills</p>'
        f'<div style="line-height:2;">{matched_html}</div>'
        f'</div>'
        f'<div>'
        f'<p class="section-label">Missing Core Skills</p>'
        f'<div style="line-height:2;">{missing_html}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    highlighted = candidate.get('Highlighted Text', '')
    if highlighted:
        with st.expander(f"🔍 JD Keywords in Resume — {candidate['File Name']}"):
            st.markdown(f"<div class='kw-preview'>{highlighted}</div>", unsafe_allow_html=True)
