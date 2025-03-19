# PDF Quiz Generator

![Project Banner](https://ocdn.eu/pulscms-transforms/1/dfuk9kpTURBXy9kMjk5NGQzMzE4MjJmOTY3ODU3ZTJhMDUzZDZmNzg3MC5qcGeTlQMAzQFFzQoozQW2lQLNBLAAw8OTCaZiMDJlN2YG3gABoTAB/quiz.jpeg)

A modern web application that generates multiple-choice quizzes with explanations from uploaded PDF documents. Built with **React** for the frontend and **FastAPI** with **CrewAI** for the backend, this tool leverages AI to create educational quizzes seamlessly.

---

## Features

- **PDF Upload**: Upload any text-based PDF to generate a quiz.
- **AI-Powered Quiz Generation**: Uses CrewAI with the Gemini LLM to create multiple-choice questions with four options, a correct answer, and detailed explanations.
- **Interactive UI**: Sleek React interface with clickable options, animations, and a responsive design.
- **Professional Design**: Clean white background with vibrant orange accents and smooth transitions.
- **Error Handling**: Robust validation for PDF content and API responses.

---

## Tech Stack

- **Frontend**: React, Axios, Framer Motion
- **Backend**: FastAPI, CrewAI, PyPDF2, Pydantic
- **AI Model**: Google Gemini (`gemini-2.0-flash`)
- **Deployment**: Local development with potential for cloud hosting

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Node.js** (v16+): [Download](https://nodejs.org/)
- **Python** (v3.9+): [Download](https://www.python.org/)
- **Git**: [Download](https://git-scm.com/)

---


# Project Setup

## Clone the Repository:
   ```bash
   git clone https://github.com/abdullah-khaled0/PDF-Quiz-Generator-with-AI-and-React.git
   cd PDF-Quiz-Generator-with-AI-and-React
```

## Create a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Install Dependencies:
```bash
pip install fastapi uvicorn PyPDF2 crewai pydantic
```

## Set Environment Variables:
Create a `.env` file in the backend directory:

```plaintext
GEMINI_API_KEY=your-gemini-api-key
```
Replace `your-gemini-api-key` with your actual Google Gemini API key.

## Run the Backend:
```bash
python crew.py
```
The server will start at [http://localhost:8000](http://localhost:8000).

---

# Frontend Setup

## Install Dependencies:
```bash
npm install
```

## Run the Frontend:
```bash
npm start
```
The React app will start at [http://localhost:3000](http://localhost:3000).

---

# Usage

### Start the Backend: 
Ensure the FastAPI server is running at [http://localhost:8000](http://localhost:8000).

### Launch the Frontend: 
Open your browser to [http://localhost:3000](http://localhost:3000).

### Upload a PDF:
1. Click **"Choose PDF"** and select a text-based PDF file.
2. Wait for the quiz to generate (a loading message will appear).

### Take the Quiz:
1. Click on any option to select an answer.
2. Press **"Submit Quiz"** to see results with explanations.
