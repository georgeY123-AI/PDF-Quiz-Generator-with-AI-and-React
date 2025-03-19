import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crewai import LLM, Agent, Crew, Process, Task
import PyPDF2 # type: ignore
import json
import logging
from pydantic import BaseModel, Field
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic models for JSON output structure
class QuizQuestion(BaseModel):
    question: str = Field(..., description="The quiz question")
    options: List[str] = Field(..., min_items=4, max_items=4, description="Four answer options")
    correctAnswer: str = Field(..., description="The correct answer")
    explanation: str = Field(..., description="Explanation of the correct answer")

class QuizOutput(BaseModel):
    questions: List[QuizQuestion] = Field(..., description="List of quiz questions")

# Load API key for Gemini
google_api_key = os.getenv("GEMINI_API_KEY")
if not google_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
llm = LLM(model="gemini/gemini-2.0-flash", temperature=0, api_key=google_api_key)

# Define Quiz Generator Agent
quiz_agent = Agent(
    role="Quiz Generator",
    goal="Analyze PDF content and generate accurate multiple-choice quizzes with explanations.",
    backstory=(
        "You are an expert in educational content creation, skilled at extracting key information from documents "
        "and transforming it into engaging multiple-choice quizzes. You ensure each question has four options, "
        "a correct answer, and a detailed explanation based on the provided content."
    ),
    llm=llm,
    verbose=True
)

# Define Quiz Generation Task with output_json
quiz_task = Task(
    description=(
        "Analyze the following PDF content and generate a multiple-choice quiz: {pdf_content}. "
        "Create as questions as possible, each with:\n"
        "1. A clear, concise question.\n"
        "2. Four distinct answer options (one correct, three plausible distractors).\n"
        "3. A correct answer.\n"
        "4. An explanation based on the PDF content.\n"
        "Return the result as a JSON object with a 'questions' key. "
        "If the content is insufficient, return {{'error': 'Insufficient content to generate a quiz.'}}."
    ),
    expected_output=(
        "A JSON object with a 'questions' array containing quiz questions, or an error message."
    ),
    agent=quiz_agent,
    output_json=QuizOutput  # Enforce JSON output with Pydantic model
)

# Define Crew
crew = Crew(
    agents=[quiz_agent],
    tasks=[quiz_task],
    verbose=True,
    process=Process.sequential
)

def run(input):
    
    try:
        logger.info(f"Running CrewAI with input: {input['pdf_content'][:100]}...")
        result = crew.kickoff(inputs=input)
        logger.info(f"Raw CrewAI result: {result}")
        
        # Handle CrewOutput object
        if hasattr(result, 'json'):  # CrewOutput with json attribute
            return json.loads(result.json)
        elif hasattr(result, 'raw'):  # Check for raw attribute as fallback
            return json.loads(result.raw)
        elif isinstance(result, dict):  # Direct dict output
            return result
        elif isinstance(result, str):  # Stringified JSON
            return json.loads(result)
        else:
            logger.error(f"Unexpected result type: {type(result)}")
            return {"error": "Invalid quiz format returned from CrewAI."}
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return {"error": "Failed to parse quiz output as JSON."}
    except Exception as e:
        logger.error(f"Error in run: {str(e)}")
        return {"error": f"Failed to generate quiz: {str(e)}"}

@app.post("/generate-quiz")
async def generate_quiz(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        logger.info("Processing uploaded PDF")
        pdf_reader = PyPDF2.PdfReader(file.file)
        pdf_content = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                pdf_content += text + "\n"
        
        if not pdf_content.strip():
            logger.warning("No readable content found in PDF")
            return {"error": "No readable content found in the PDF. Please upload a valid document."}
        
        logger.info(f"Extracted PDF content: {pdf_content[:100]}...")
        input_data = {"pdf_content": pdf_content}
        quiz_result = run(input_data)
        logger.info(f"Quiz result: {quiz_result}")
        return quiz_result
    
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("crew:app", host="0.0.0.0", port=8000, reload=True)