import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import time
from wordcloud import WordCloud

from utils.nlp_engine import process_all_resumes
from utils.ui_components import (
    apply_custom_css, render_hero, render_how_it_works,
    render_metrics_row, render_top3_spotlight, render_candidate_card,
    render_section_header, render_divider
)
from utils.pdf_generator import generate_pdf_report
from utils.db_engine import save_analysis_to_db, get_analysis_history
import json

st.set_page_config(
    page_title="CareerRank AI | Smart Candidate Screening",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_css()

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    gemini_key = st.text_input("Gemini API Key", type="password", placeholder="AI Interview Questions", help="Get a free key from Google AI Studio to unlock generative interview questions.")
    if gemini_key:
        st.session_state.gemini_api_key = gemini_key

    st.markdown("### 🗄️ Database (Supabase)")
    sb_url = st.text_input("Supabase Project URL", placeholder="https://xyz.supabase.co")
    sb_key = st.text_input("Supabase API Key", type="password")
    if sb_url and sb_key:
        st.session_state.supabase_url = sb_url
        st.session_state.supabase_key = sb_key
        
        st.markdown("#### 📜 History")
        history = get_analysis_history()
        if history:
            for item in history:
                with st.expander(f"JD: {item.get('job_description', '')[:20]}..."):
                    try:
                        res = json.loads(item.get("results", "[]"))
                        for r in res:
                            st.write(f"#{r['rank']} {r['name']} - {r['score']}%")
                    except:
                        st.write("Error parsing results.")
        else:
            st.info("No history found in database.")

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = ""

def generate_wordcloud(results):
    all_skills = []
    for r in results:
        all_skills.extend(r.get('Matched Skills', []))
        all_skills.extend(r.get('JD Skills', []))
    if not all_skills:
        return None
    wc = WordCloud(
        width=700, height=340,
        background_color=None, mode="RGBA",
        colormap="cool", max_words=60, prefer_horizontal=0.85,
    ).generate(" ".join(all_skills))
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    fig.patch.set_alpha(0)
    plt.tight_layout(pad=0)
    return fig

def prepare_export_df(filtered_df):
    export_df = filtered_df.copy()
    for col_name in ["Matched Skills", "Missing Skills", "Extracted Skills", "JD Skills"]:
        if col_name in export_df.columns:
            export_df[col_name] = export_df[col_name].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )
    return export_df.drop(columns=["Highlighted Text"], errors="ignore")

def main():
    
    render_hero()

    render_divider()
    render_how_it_works()

    render_divider()
    render_section_header(
        "🖊️ Set Up Your Analysis",
        "Paste a job description and upload candidate resumes to begin"
    )

    input_col1, input_col2 = st.columns([1, 1], gap="large")

    with input_col1:
        st.markdown("""
            <div class="input-section-label">
                <span class="input-icon">📝</span> Job Description
            </div>
        """, unsafe_allow_html=True)
        jd_input = st.text_area(
            "Job Description",
            height=280,
            value=st.session_state.jd_text,
            placeholder="e.g. We are looking for a Python Developer with 3+ years of experience in Django, AWS, and PostgreSQL…",
            label_visibility="collapsed",
            key="jd_textarea"
        )
        st.session_state.jd_text = jd_input

    with input_col2:
        st.markdown("""
            <div class="input-section-label">
                <span class="input-icon">📄</span> Upload Resumes
            </div>
        """, unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Upload PDF resumes",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="resume_uploader"
        )
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) ready for analysis.")
            for f in uploaded_files:
                st.markdown(
                    f"<p class='file-chip'>📎 {f.name}</p>",
                    unsafe_allow_html=True
                )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        analyze_btn = st.button(
            "🚀 Analyze & Rank Candidates",
            use_container_width=True,
            key="analyze_btn"
        )

    if analyze_btn:
        if not jd_input.strip():
            st.error("⚠️ Please paste a Job Description first.")
        elif not uploaded_files:
            st.error("⚠️ Please upload at least one resume PDF.")
        else:
            with st.spinner("🤖 AI is analysing and ranking candidates…"):
                prog = st.progress(0)
                for i in range(40):
                    time.sleep(0.01)
                    prog.progress(i + 1)
                results = process_all_resumes(uploaded_files, jd_input)
                st.session_state.analysis_results = results
                for i in range(40, 100):
                    time.sleep(0.005)
                    prog.progress(i + 1)
                prog.empty()
            st.toast("✅ Analysis complete!", icon="🎉")
            
            # Save to Database if connected
            if st.session_state.get('supabase_url') and st.session_state.get('supabase_key'):
                if save_analysis_to_db(jd_input, results):
                    st.toast("💾 Saved to Supabase History!", icon="☁️")
                else:
                    st.error("Failed to save to Supabase. Check your Table structure.")

    if not st.session_state.analysis_results:
        return

    results = st.session_state.analysis_results
    df      = pd.DataFrame(results)

    avg_score   = df["Match Score"].mean()
    top_cand    = results[0] if results else None
    shortlisted = len(df[df["Match Score"] >= 75])
    top_name    = top_cand.get("Candidate Name", top_cand["File Name"]) if top_cand else "N/A"
    top_score   = top_cand["Match Score"] if top_cand else None

    render_divider(large=True)
    render_section_header(
        "📊 Ranking Dashboard",
        "AI-powered results sorted from highest to lowest match score"
    )

    render_metrics_row(len(results), avg_score, top_name, top_score, shortlisted)

    if len(results) >= 2:
        render_divider()
        render_top3_spotlight(results)

    render_divider()
    render_section_header("🔍 Visual Analysis", "Score distribution and skill coverage at a glance")

    chart_col, wc_col = st.columns([1, 1], gap="large")

    with chart_col:
        st.markdown("<p class='card-title'>📊 Match Score Distribution</p>", unsafe_allow_html=True)
        fig = px.bar(
            df,
            x="Candidate Name" if "Candidate Name" in df.columns else "File Name",
            y="Match Score",
            color="Match Score",
            color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
            range_color=[0, 100],
            text="Match Score",
            custom_data=["File Name"],
        )
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>File: %{customdata[0]}<br>Score: %{y:.1f}%<extra></extra>"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="#F8FAFC",
            margin=dict(l=10, r=10, t=20, b=80),
            xaxis_title="",
            yaxis_title="Score (%)",
            yaxis_range=[0, 110],
            coloraxis_showscale=False,
            xaxis_tickangle=-30,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    with wc_col:
        st.markdown("<p class='card-title'>☁️ Skill Word Cloud</p>", unsafe_allow_html=True)
        wc_fig = generate_wordcloud(results)
        if wc_fig:
            st.pyplot(wc_fig, use_container_width=True)
            plt.close(wc_fig)
        else:
            st.info("Not enough skill data to generate a word cloud.")

    render_divider()
    render_section_header("📋 Full Rankings", "Filter, review and compare all candidates in detail")

    min_score        = st.slider("Minimum Match Score Filter", 0, 100, 0, key="score_filter",
                                  format="%d%%")
    filtered_results = [r for r in results if r["Match Score"] >= min_score]
    filtered_df      = df[df["Match Score"] >= min_score].copy()

    if filtered_results:
        st.markdown(
            f"<p style='color:#64748B;font-size:0.82rem;margin:6px 0 16px;'>"
            f"Showing {len(filtered_results)} of {len(results)} candidate(s)"
            f"</p>",
            unsafe_allow_html=True
        )
        for cand in filtered_results:
            render_candidate_card(cand)
    else:
        st.info("No candidates meet the selected score threshold. Try lowering the filter.")

    render_divider()
    render_section_header("📥 Export Results", "Download the full ranked report in your preferred format")

    export_df  = prepare_export_df(filtered_df)
    csv_data   = export_df.to_csv(index=False).encode('utf-8')

    exp_col1, exp_col2 = st.columns([1, 1], gap="large")

    with exp_col1:
        st.markdown("<p class='card-title'>CSV Spreadsheet</p>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#94A3B8;font-size:0.82rem;margin:0 0 12px;'>"
            "All candidates with scores, skills, and recommendations in a spreadsheet-ready format."
            "</p>",
            unsafe_allow_html=True
        )
        st.download_button(
            label="⬇️ Download CSV Report",
            data=csv_data,
            file_name="careerrank_results.csv",
            mime="text/csv",
            use_container_width=True,
            key="csv_dl"
        )

    with exp_col2:
        st.markdown("<p class='card-title'>PDF Summary Report</p>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#94A3B8;font-size:0.82rem;margin:0 0 12px;'>"
            "Branded recruiter report with abstract, methodology, rankings, and conclusion."
            "</p>",
            unsafe_allow_html=True
        )
        try:
            pdf_bytes = generate_pdf_report(filtered_df, len(results), top_cand, avg_score)
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name="careerrank_summary_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="pdf_dl"
            )
        except Exception as e:
            st.warning(f"PDF could not be generated: {e}")

    st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
