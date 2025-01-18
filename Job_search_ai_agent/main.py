from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.file import FileTools
import PyPDF2
import io
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
resume_agent = Agent(
    name="Resume Analyzer",
    role="Analyze resumes and extract key information",
    model=OpenAIChat(id="gpt-4"),
    tools=[FileTools()],
    instructions=[
        "Extract key skills, experience, and qualifications from resumes",
        "Provide structured output in JSON format",
        "Consider both technical and soft skills",
    ],
    show_tool_calls=True,
    markdown=True,
)

job_search_agent = Agent(
    name="Job Search Agent",
    role="Search for relevant job postings",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGo()],
    instructions=[
        "Search for job postings that match the candidate's profile",
        "Focus on recent postings",
        "Include direct links to job postings",
        "Evaluate job requirements against candidate skills",
    ],
    show_tool_calls=True,
    markdown=True,
)

# HTML template as a string
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Job Search Assistant</title>
    <style>
        /* Your CSS styles here */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 2rem;
        }

        .upload-area {
            border: 2px dashed #3498db;
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
            background-color: white;
            cursor: pointer;
            margin-bottom: 1rem;
        }

        .upload-area.drag-over {
            border-color: #2ecc71;
            background-color: #e8f5e9;
        }

        .hidden {
            display: none;
        }

        .button {
            background-color: #3498db;
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        .button:disabled {
            background-color: #bdc3c7;
            cursor: not-allowed;
        }

        .results {
            margin-top: 2rem;
            padding: 1rem;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .error {
            color: #e74c3c;
            padding: 1rem;
            background-color: #fdeaea;
            border-radius: 4px;
            margin: 1rem 0;
        }

        .loading {
            text-align: center;
            padding: 2rem;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Job Search Assistant</h1>
        
        <div class="upload-container">
            <div class="upload-area" id="dropZone">
                <p>Drag & drop your resume here or click to select</p>
                <input type="file" id="fileInput" accept=".pdf" style="display: none;">
            </div>
            
            <div id="fileInfo" class="hidden">
                <p>Selected file: <span id="fileName"></span></p>
                <button id="analyzeButton" class="button">Analyze Resume</button>
            </div>
        </div>

        <div id="loading" class="loading hidden">
            <div class="spinner"></div>
            <p>Analyzing your resume...</p>
        </div>

        <div id="error" class="error hidden"></div>

        <div id="results" class="results hidden">
            <h2>Analysis Results</h2>
            <div id="profileContent"></div>
            <div id="jobMatches"></div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            const fileInfo = document.getElementById('fileInfo');
            const fileName = document.getElementById('fileName');
            const analyzeButton = document.getElementById('analyzeButton');
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const results = document.getElementById('results');
            const profileContent = document.getElementById('profileContent');
            const jobMatches = document.getElementById('jobMatches');

            // Prevent default drag behaviors
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, preventDefaults, false);
                document.body.addEventListener(eventName, preventDefaults, false);
            });

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            // Handle file drop
            dropZone.addEventListener('drop', handleDrop);
            dropZone.addEventListener('dragover', () => dropZone.classList.add('drag-over'));
            dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));

            // Handle file selection
            fileInput.addEventListener('change', (e) => handleFiles(e.target.files));
            dropZone.addEventListener('click', () => fileInput.click());

            function handleDrop(e) {
                const dt = e.dataTransfer;
                const files = dt.files;
                handleFiles(files);
            }

            function handleFiles(files) {
                if (files.length > 0) {
                    const file = files[0];
                    if (file.type === 'application/pdf') {
                        fileName.textContent = file.name;
                        fileInfo.classList.remove('hidden');
                        error.classList.add('hidden');
                        analyzeButton.onclick = () => analyzePDF(file);
                    } else {
                        showError('Please upload a PDF file');
                    }
                }
            }

            async function analyzePDF(file) {
                try {
                    loading.classList.remove('hidden');
                    error.classList.add('hidden');
                    results.classList.add('hidden');
                    analyzeButton.disabled = true;

                    const formData = new FormData();
                    formData.append('file', file);

                    const response = await fetch('/analyze-resume', {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        throw new Error('Failed to analyze resume');
                    }

                    const data = await response.json();
                    
                    profileContent.innerHTML = `
                        <h3>Profile</h3>
                        <pre>${JSON.stringify(data.profile, null, 2)}</pre>
                    `;
                    
                    jobMatches.innerHTML = `
                        <h3>Job Matches</h3>
                        ${data.job_matches}
                    `;

                    results.classList.remove('hidden');
                } catch (err) {
                    showError(err.message);
                } finally {
                    loading.classList.add('hidden');
                    analyzeButton.disabled = false;
                }
            }

            function showError(message) {
                error.textContent = message;
                error.classList.remove('hidden');
            }
        });
    </script>
</body>
</html>
"""

def process_resume_file(file_content):
    """Process resume file (PDF) and extract text"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error processing resume: {str(e)}")

def analyze_resume(resume_content):
    """Analyze the resume and extract key information"""
    analysis_prompt = f"""
    Analyze the following resume and extract key information:
    {resume_content}
    
    Please provide:
    1. Key technical skills
    2. Years of experience
    3. Primary job roles
    4. Industry expertise
    5. Education level
    
    Format the output as JSON.
    """
    
    result = resume_agent.run(analysis_prompt)
    try:
        return json.loads(result.content)
    except json.JSONDecodeError:
        return {"text": result.content}

def search_jobs(profile):
    """Search for relevant jobs based on the resume analysis"""
    search_prompt = f"""
    Find relevant job postings for a candidate with the following profile:
    {json.dumps(profile, indent=2)}
    
    Focus on:
    1. Skills match
    2. Experience level match
    3. Industry relevance
    4. Recent postings (last 30 days)
    
    Return results as HTML with direct links to job postings.
    Include company name, job title, location, and key requirements.
    Format the results in a clean, easy-to-read way with proper HTML styling.
    """
    
    result = job_search_agent.run(search_prompt)
    return result.content

@app.get("/")
async def home():
    return HTMLResponse(content=HTML_CONTENT)

@app.post("/analyze-resume")
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        content = await file.read()
        resume_text = process_resume_file(content)
        profile = analyze_resume(resume_text)
        job_matches = search_jobs(profile)
        
        return {
            "profile": profile,
            "job_matches": job_matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)