# AI Document Red Alert Detection System

## Project Overview

AI Document Red Alert Detection System is an AI-powered web application that scans uploaded documents and detects suspicious, sensitive, fraudulent, threatening, or policy-violating content.

The system extracts text from uploaded files, analyzes the content using NLP and rule-based AI detection methods, generates a risk score, assigns an alert level, highlights suspicious sections, and stores document history for future review.

## Area of Study

This project belongs to the following areas:

- Artificial Intelligence
- Natural Language Processing
- Document Intelligence
- Cybersecurity
- Information Security
- Fraud Detection
- OCR-Based Text Analysis

## Key Features

- User registration and JWT login
- PDF, DOCX, TXT, and image upload
- OCR support for scanned image documents
- English and Gujarati risky content detection
- Suspicious keyword detection
- Sensitive information detection
- Threat language detection
- Policy violation detection
- Indian compliance data detection
- Tampered or abnormal text detection
- Risk score generation
- Green, Yellow, and Red alert classification
- AI-generated document summary
- Highlighted suspicious sections
- Document history
- Admin panel
- Dashboard analytics and charts

## Alert Levels

| Risk Score | Alert Level |
|---|---|
| 0-30 | Green |
| 31-70 | Yellow |
| 71-100 | Red |

## Tech Stack

### Backend

- Python
- FastAPI
- MongoDB
- PyMongo Async
- JWT Authentication
- Pydantic
- pdfplumber
- python-docx
- pytesseract
- Pillow

### Frontend

- React
- Vite
- Axios
- Lucide React
- Recharts
- CSS

### AI/NLP

- Rule-based NLP detection
- Keyword matching
- Regular expressions
- OCR text extraction
- Risk scoring engine

## Project Structure

```text
ai-document-red-alert-project
├── backend
│   ├── app
│   │   ├── ai
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   ├── document_processing
│   │   ├── repositories
│   │   ├── schemas
│   │   ├── services
│   │   └── main.py
│   ├── uploads
│   ├── requirements.txt
│   └── .env
├── frontend
│   ├── src
│   │   ├── api
│   │   ├── pages
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── .env
├── sample_documents
└── README.md`

### How the System Works
- User logs in using JWT authentication.
- User uploads a document.
- Backend validates the file type and size.
- Text is extracted from the document.
- OCR is applied if the file is an image.
- AI pipeline analyzes the extracted text.
- Risk score is calculated.
- Alert level is assigned.
- Suspicious sections are highlighted.
- Result is stored in MongoDB.
- React dashboard displays the analysis.