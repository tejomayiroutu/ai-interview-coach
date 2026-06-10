import streamlit as st

from utils.pdf_parser import extract_text
from agents.question_generator import generate_questions
from agents.interview_evaluator import evaluate_interview


st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom styling (UI only)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        .section-header {
            font-size: 1.35rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        .section-caption {
            color: #6b7280;
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }
        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }
        div[data-testid="stSidebar"] .stMarkdown p,
        div[data-testid="stSidebar"] .stMarkdown li,
        div[data-testid="stSidebar"] .stMarkdown h1,
        div[data-testid="stSidebar"] .stMarkdown h2,
        div[data-testid="stSidebar"] .stMarkdown h3 {
            color: #f1f5f9;
        }
        .hero-badge {
            display: inline-block;
            background: #e0f2fe;
            color: #0369a1;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        .question-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("# 🎯 AI Interview Coach")
    st.markdown(
        "Run a full mock interview with 10 personalized questions "
        "tailored to your resume, target company, role, and difficulty."
    )
    st.divider()
    st.markdown("### 📋 How to Use")
    st.markdown(
        """
        1. **Upload your resume** — PDF format only.
        2. **Review extracted text** — Confirm your resume was read correctly.
        3. **Set up the interview** — Choose company, role, and difficulty.
        4. **Generate questions** — Get 10 personalized interview prompts.
        5. **Answer questions** — Fill in as many answers as you like (all optional).
        6. **Submit interview** — Receive a full performance report with scores.
        """
    )
    st.divider()
    st.info(
        "💡 Tip: You don't need to answer every question — "
        "but skipped questions will reduce your coverage score."
    )

# ---------------------------------------------------------------------------
# Main header
# ---------------------------------------------------------------------------
st.markdown('<p class="hero-badge">AI-Powered Mock Interview</p>', unsafe_allow_html=True)
st.title("Welcome to Your Interview Coach")
st.markdown(
    "Upload your resume, configure your interview settings, and complete "
    "a full mock interview with detailed AI feedback."
)

st.divider()

# ---------------------------------------------------------------------------
# Section 1: Resume Upload
# ---------------------------------------------------------------------------
st.markdown('<p class="section-header">📄 Resume Upload</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-caption">Start by uploading your resume in PDF format.</p>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"],
        help="Only PDF files are supported.",
    )

    if uploaded_file is None:
        st.info("👆 Upload a PDF resume to begin your mock interview session.")

if uploaded_file is not None:

    with st.spinner("Extracting resume..."):
        resume_text = extract_text(uploaded_file)

    st.success("✅ Resume processed successfully!")

    with st.expander("📖 View Extracted Resume", expanded=False):
        st.text_area(
            "Resume Content",
            resume_text,
            height=300,
        )

    st.divider()

    # -----------------------------------------------------------------------
    # Section 2: Interview Setup
    # -----------------------------------------------------------------------
    st.markdown('<p class="section-header">⚙️ Interview Setup</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-caption">Select the company, role, and difficulty for your mock interview.</p>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            company = st.selectbox(
                "Target Company",
                [
                    "Infosys",
                    "TCS",
                    "Wipro",
                    "Amazon",
                    "Google",
                    "Microsoft",
                ],
            )

        with col2:
            role = st.selectbox(
                "Target Role",
                [
                    "Software Engineer",
                    "AI/ML Engineer",
                    "Full Stack Developer",
                    "Data Analyst",
                ],
            )

        with col3:
            difficulty = st.selectbox(
                "Difficulty",
                ["Easy", "Medium", "Hard"],
            )

        st.markdown("")
        generate_col1, generate_col2, generate_col3 = st.columns([1, 1, 2])
        with generate_col1:
            generate_clicked = st.button(
                "✨ Generate Interview Questions",
                type="primary",
                use_container_width=True,
            )

    if generate_clicked:

        with st.spinner("Generating 10 personalized questions..."):
            questions = generate_questions(
                resume_text,
                company,
                role,
                difficulty,
            )

        for i in range(10):
            st.session_state.pop(f"answer_{i}", None)

        st.session_state["questions"] = questions
        st.session_state.pop("interview_report", None)
        st.success(
            f"10 **{difficulty}** questions generated for **{role}** at **{company}**!"
        )

    if "questions" in st.session_state:

        questions = st.session_state["questions"]

        st.divider()

        # -------------------------------------------------------------------
        # Section 3: Mock Interview
        # -------------------------------------------------------------------
        st.markdown('<p class="section-header">📝 Mock Interview</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-caption">Answer any number of questions below — all answers are optional.</p>',
            unsafe_allow_html=True,
        )

        answers = []

        with st.container(border=True):
            for i, question in enumerate(questions):
                st.markdown(f"**Question {i + 1}**")
                st.markdown(question)
                answer = st.text_area(
                    f"Answer for question {i + 1}",
                    key=f"answer_{i}",
                    height=120,
                    placeholder="Type your answer here (optional)...",
                    label_visibility="collapsed",
                )
                answers.append(answer)
                if i < len(questions) - 1:
                    st.divider()

        st.markdown("")
        submit_col1, submit_col2, submit_col3 = st.columns([1, 1, 2])
        with submit_col1:
            submit_clicked = st.button(
                "📊 Submit Mock Interview",
                type="primary",
                use_container_width=True,
            )

        if submit_clicked:

            with st.spinner("Evaluating your mock interview..."):
                report = evaluate_interview(questions, answers)

            st.session_state["interview_report"] = report

        if "interview_report" in st.session_state:

            report = st.session_state["interview_report"]

            st.divider()

            # ---------------------------------------------------------------
            # Section 4: Interview Report
            # ---------------------------------------------------------------
            st.markdown('<p class="section-header">📊 Interview Summary</p>', unsafe_allow_html=True)

            with st.container(border=True):
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

                with stat_col1:
                    st.metric(
                        "Questions Generated",
                        report["questions_generated"],
                    )
                with stat_col2:
                    st.metric(
                        "Questions Attempted",
                        report["questions_attempted"],
                    )
                with stat_col3:
                    st.metric(
                        "Questions Skipped",
                        report["questions_skipped"],
                    )
                with stat_col4:
                    st.metric(
                        "Coverage Score",
                        f"{report['coverage_score']:.0f}%",
                    )

            if report.get("evaluation") is None:
                st.warning(f"⚠️ {report.get('message', 'No evaluation available.')}")
            else:
                st.divider()
                st.markdown('<p class="section-header">📋 Performance Report</p>', unsafe_allow_html=True)

                with st.container(border=True):
                    score_col1, score_col2, score_col3 = st.columns(3)

                    with score_col1:
                        st.info(f"**Overall Score**\n\n{report['overall_score']}")
                    with score_col2:
                        st.info(f"**Technical Knowledge Score**\n\n{report['technical_score']}")
                    with score_col3:
                        st.info(f"**Communication Score**\n\n{report['communication_score']}")

                    st.markdown("")

                    with st.expander("💪 Strengths", expanded=True):
                        st.markdown(report["strengths"])

                    with st.expander("🔍 Weaknesses", expanded=True):
                        st.markdown(report["weaknesses"])

                    with st.expander("📚 Topics Needing Improvement", expanded=True):
                        st.markdown(report["topics"])

                    st.success(f"**Hiring Recommendation**\n\n{report['hiring_recommendation']}")

                    with st.expander("📄 Full Evaluation Report", expanded=False):
                        st.markdown(report["evaluation"])
