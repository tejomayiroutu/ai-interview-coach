from utils.llm import generate_response


def evaluate_answer(question, answer):
    prompt = f"""
You are an experienced technical interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return the response in exactly this format:

Score: X/10

Strengths:
- point 1
- point 2

Missing Points:
- point 1
- point 2

Suggested Answer:
<Provide an improved answer suitable for an interview>
"""

    return generate_response(prompt)