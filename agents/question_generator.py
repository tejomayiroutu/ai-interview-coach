from utils.llm import generate_response


def generate_questions(resume_text, company, role):
    prompt = f"""
You are an experienced technical interviewer.

Candidate Resume:
{resume_text}

Target Company:
{company}

Target Role:
{role}

Generate exactly 10 interview questions.

Requirements:

1. 3 questions based on the candidate's projects and skills.
2. 2 DSA questions appropriate for {company}.
3. 1 DBMS question.
4. 1 Operating Systems question.
5. 1 Computer Networks question.
6. 2 HR/Behavioral questions.

The questions should match the difficulty level typically expected for {company} interviews.

Return ONLY the numbered questions.
"""

    return generate_response(prompt)