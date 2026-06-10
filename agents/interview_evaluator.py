import re

from utils.llm import generate_response


def _build_qa_block(questions, answers):
    block = ""
    for i, (question, answer) in enumerate(zip(questions, answers)):
        if answer and answer.strip():
            block += (
                f"\nQuestion {i + 1}:\n{question}\n\n"
                f"Answer:\n{answer.strip()}\n\n---\n"
            )
    return block


def _parse_section(text, heading):
    pattern = rf"{heading}:\s*\n(.*?)(?=\n[A-Z][^\n]*:\s*\n|\Z)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def _parse_score(text, label):
    match = re.search(rf"{label}:\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
    return match.group(1).strip() if match else "N/A"


def evaluate_interview(questions, answers):
    total = len(questions)
    attempted = sum(1 for a in answers if a and a.strip())
    skipped = total - attempted
    coverage = (attempted / total) * 100 if total else 0

    stats = {
        "questions_generated": total,
        "questions_attempted": attempted,
        "questions_skipped": skipped,
        "coverage_score": coverage,
    }

    if attempted == 0:
        return {
            **stats,
            "evaluation": None,
            "message": "No answers provided. Please answer at least one question.",
        }

    qa_block = _build_qa_block(questions, answers)

    prompt = f"""
You are an experienced technical interviewer conducting a mock interview debrief.

Interview Statistics:
- Questions Generated: {total}
- Questions Attempted: {attempted}
- Questions Skipped: {skipped}
- Coverage Score: {coverage:.0f}%

The candidate skipped {skipped} out of {total} questions.
Apply an appropriate penalty to the overall assessment due to incomplete coverage.
A lower coverage score should result in a lower overall score and a more cautious
hiring recommendation.

Answered Questions and Responses:
{qa_block}

Evaluate ONLY the answered questions above, then provide a comprehensive report.

Return the response in exactly this format:

Overall Score: X/10
Technical Knowledge Score: X/10
Communication Score: X/10

Strengths:
- point 1
- point 2

Weaknesses:
- point 1
- point 2

Topics Needing Improvement:
- topic 1
- topic 2

Hiring Recommendation:
<Clear hire / no-hire / maybe recommendation with brief justification>
"""

    raw_evaluation = generate_response(prompt)

    return {
        **stats,
        "evaluation": raw_evaluation,
        "overall_score": _parse_score(raw_evaluation, "Overall Score"),
        "technical_score": _parse_score(raw_evaluation, "Technical Knowledge Score"),
        "communication_score": _parse_score(raw_evaluation, "Communication Score"),
        "strengths": _parse_section(raw_evaluation, "Strengths"),
        "weaknesses": _parse_section(raw_evaluation, "Weaknesses"),
        "topics": _parse_section(raw_evaluation, "Topics Needing Improvement"),
        "hiring_recommendation": _parse_section(raw_evaluation, "Hiring Recommendation"),
    }
