# LegalEase

## AI-Powered Legal Document Generator

LegalEase is an AI-assisted legal document drafting application built using:

- Python
- Streamlit
- FastAPI
- Google Gemini
- python-docx
- ReportLab
- Pydantic

## Features

- AI legal-document drafting
- NDA generation
- Employment contract generation
- Lease agreement generation
- Service agreement generation
- Editable document
- TXT export
- DOCX export
- PDF export
- Company logo support
- FastAPI REST API
- Gemini AI integration
- Automated API tests

## Project Structure

LegalEase/

backend/

    main.py
    routes.py
    schemas.py
    config.py
    dependencies.py

    ai_core/

        gemini_generator.py

    formatters/

        text_formatter.py
        docx_formatter.py
        pdf_formatter.py

frontend/

    app.py

tests/

    test_api.py

assets/

requirements.txt
.env
.env.example
Dockerfile
Procfile
README.md


# Installation

## Step 1

Open the project in VS Code.

## Step 2

Create a virtual environment.

Windows:

python -m venv .venv

Activate:

.venv\Scripts\activate

macOS/Linux:

python3 -m venv .venv

source .venv/bin/activate


# Step 3

Install dependencies:

pip install -r requirements.txt


# Step 4

Create .env

Copy:

.env.example

to:

.env

Then enter your Gemini API key.


# Step 5

Start FastAPI

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000


# Step 6

Open another terminal.

Activate the virtual environment again if required.

Start Streamlit:

streamlit run frontend/app.py


# Step 7

Open:

http://localhost:8501


# API

FastAPI documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health


# Testing

Run:

pytest -q


# Legal Notice

LegalEase is an AI-assisted drafting tool.

Generated documents may contain errors or omissions.

Always review generated legal documents carefully
and obtain qualified legal advice when appropriate.