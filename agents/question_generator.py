import re

from utils.llm import generate_response


def _parse_questions(text):
    """Parse numbered questions (1. ... 10.) from LLM response."""
    matches = re.findall(
        r"(?:^|\n)\d+\.\s*(.+?)(?=\n\d+\.\s|\Z)",
        text.strip(),
        re.DOTALL,
    )
    return [m.strip() for m in matches if m.strip()]


def generate_questions(resume_text, company, role, difficulty):
    prompt = f"""
You are an experienced technical interviewer.

Candidate Resume:
{resume_text}

Target Company:
{company}

Target Role:
{role}

Difficulty Level:
{difficulty}

Generate exactly 10 interview questions at {difficulty} difficulty.

Requirements:

1. 3 questions based on the candidate's projects and skills.
2. 2 DSA questions appropriate for {company} at {difficulty} level.
3. 1 DBMS question.
4. 1 Operating Systems question.
5. 1 Computer Networks question.
6. 2 HR/Behavioral questions.

All questions must match the {difficulty} difficulty level and the expectations
for {role} interviews at {company}.

Return ONLY the 10 numbered questions (1. through 10.), one per line.
Do not include any other text.
"""

    raw = generate_response(prompt)
    questions = _parse_questions(raw)

    if len(questions) < 10:
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        numbered = [
            re.sub(r"^\d+\.\s*", "", line).strip()
            for line in lines
            if re.match(r"^\d+\.", line)
        ]
        if len(numbered) > len(questions):
            questions = numbered

    return questions[:10]
