import streamlit as st

from utils.pdf_parser import extract_text
from agents.question_generator import generate_questions
from agents.evaluator import evaluate_answer


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
        "Practice for your next interview with AI-generated questions "
        "tailored to your resume, target company, and role."
    )
    st.divider()
    st.markdown("### 📋 How to Use")
    st.markdown(
        """
        1. **Upload your resume** — PDF format only.
        2. **Review extracted text** — Confirm your resume was read correctly.
        3. **Set up the interview** — Choose company and role.
        4. **Generate questions** — Get personalized interview prompts.
        5. **Practice & evaluate** — Paste a question, write your answer, and receive feedback.
        """
    )
    st.divider()
    st.info(
        "💡 Tip: Copy one question at a time into the evaluation section "
        "for focused practice."
    )

# ---------------------------------------------------------------------------
# Main header
# ---------------------------------------------------------------------------
st.markdown('<p class="hero-badge">AI-Powered Interview Preparation</p>', unsafe_allow_html=True)
st.title("Welcome to Your Interview Coach")
st.markdown(
    "Upload your resume, configure your target role, and get actionable "
    "feedback to sharpen your interview skills."
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
        st.info("👆 Upload a PDF resume to begin your interview preparation session.")

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
        '<p class="section-caption">Select the company and role you are preparing for.</p>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        col1, col2 = st.columns(2)

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

        st.markdown("")
        generate_col1, generate_col2, generate_col3 = st.columns([1, 1, 2])
        with generate_col1:
            generate_clicked = st.button(
                "✨ Generate Interview Questions",
                type="primary",
                use_container_width=True,
            )

    if generate_clicked:

        with st.spinner("Generating personalized questions..."):
            questions = generate_questions(
                resume_text,
                company,
                role,
            )

        st.session_state["questions"] = questions
        st.success(f"Questions generated for **{role}** at **{company}**!")

    if "questions" in st.session_state:

        st.divider()

        # -------------------------------------------------------------------
        # Section 3: Generated Questions
        # -------------------------------------------------------------------
        st.markdown('<p class="section-header">📝 Generated Questions</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-caption">Review your personalized interview questions below.</p>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            with st.expander("💬 View Interview Questions", expanded=True):
                st.markdown(st.session_state["questions"])

        st.divider()

        # -------------------------------------------------------------------
        # Section 4: Answer Evaluation
        # -------------------------------------------------------------------
        st.markdown('<p class="section-header">🎤 Answer Evaluation</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-caption">Paste a question, write your answer, and get AI feedback.</p>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            question = st.text_input(
                "Paste one interview question",
                placeholder="e.g. Tell me about a challenging project you worked on.",
            )

            answer = st.text_area(
                "Enter your answer",
                height=200,
                placeholder="Write your response here as you would in a real interview...",
            )

            eval_col1, eval_col2, eval_col3 = st.columns([1, 1, 2])
            with eval_col1:
                evaluate_clicked = st.button(
                    "📊 Evaluate Answer",
                    type="primary",
                    use_container_width=True,
                )

        if evaluate_clicked:

            if question and answer:

                with st.spinner("Evaluating answer..."):
                    feedback = evaluate_answer(
                        question,
                        answer,
                    )

                st.markdown('<p class="section-header">📊 Feedback</p>', unsafe_allow_html=True)

                with st.container(border=True):
                    st.success("Evaluation complete! Review your feedback below.")
                    with st.expander("📋 Detailed Feedback", expanded=True):
                        st.markdown(feedback)

            else:
                st.warning(
                    "⚠️ Please provide both the question and your answer before evaluating."
                )
