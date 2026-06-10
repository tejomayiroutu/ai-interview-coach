# AI Interview Coach Agent

## Overview

AI Interview Coach is an LLM-powered interview preparation assistant that analyzes a candidate's resume and generates personalized interview questions tailored to specific companies and job roles. It also evaluates candidate responses and provides constructive feedback.

## Features

* Resume PDF upload and text extraction
* Company-specific interview question generation
* Role-based interview customization
* Project-focused technical questions
* AI-powered answer evaluation
* Personalized interview feedback

## Tech Stack

* Python
* Streamlit
* Groq API
* Llama 3.3 70B Versatile
* pdfplumber
* python-dotenv

## Workflow

Resume Upload → Resume Parsing → Question Generation → Answer Submission → AI Evaluation → Feedback Generation

## Future Enhancements

* Voice-based mock interviews
* LangGraph integration
* Adaptive difficulty levels
* Interview progress tracking

## How to Run

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Create a `.env` file and add your Groq API key.
4. Run `streamlit run app.py`.
