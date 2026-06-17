import os
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from PyPDF2 import PdfReader
from google import genai

# Import your model (Ensure you have this in models.py as per previous step)
from .models import ResumeAnalysis

# --- GEMINI CONFIGURATION ---
# It's recommended to set this as an environment variable
API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
client = genai.Client(api_key=API_KEY)

# --- HELPER FUNCTIONS ---

def parse_ai_response(text):
    """Parses raw Gemini text into a structured dictionary for the UI."""
    data = {
        "score": 0,
        "strengths": [],
        "weaknesses": [],
        "improvements": []
    }
    
    # 1. Extract Score (e.g., Score: 85/100)
    score_match = re.search(r"Score:\s*(\d+)", text)
    if score_match:
        data["score"] = int(score_match.group(1))

    # 2. Helper to extract bullet points under specific headers
    def get_bullets(section_name, full_text):
        pattern = rf"{section_name}:(.*?)(?:Weaknesses:|Improvements:|Resume Text:|$)"
        match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
        if match:
            section_content = match.group(1).strip()
            bullets = re.findall(r"(?:^|\n)[-*•\d\.]+\s*(.+)", section_content)
            return [b.strip() for b in bullets]
        return []

    data["strengths"] = get_bullets("Strengths", text)
    data["weaknesses"] = get_bullets("Weaknesses", text)
    data["improvements"] = get_bullets("Improvements", text)
    
    return data



def signup_view(request):
    """Handles new user registration."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to Smart Recruiter.")
            return redirect('index')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
\

@login_required
def index(request):
    results = None
    error = None

    if request.method == "POST" and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        # Capture the new job description field
        job_description = request.POST.get('job_description', 'General Industry Standards')
        
        if not resume_file.name.endswith('.pdf'):
            error = "Invalid format. Please upload a PDF file."
        else:
            try:
                # 1. Extract Text from PDF
                reader = PdfReader(resume_file)
                resume_text = "".join([page.extract_text() for page in reader.pages])
                
                if not resume_text.strip():
                    error = "Could not extract text. Your PDF might be an image-based scan."
                else:
                    # 2. Updated AI Analysis with JD context
                    raw_analysis = analyze_resume_ai(resume_text, job_description)
                    
                    # 3. Parse for UI
                    results = parse_ai_response(raw_analysis)
                    
                    # 4. Save to Database (including JD context if you update your model)
                    ResumeAnalysis.objects.create(
                        user=request.user,
                        filename=resume_file.name,
                        score=results['score'],
                        raw_response=raw_analysis
                    )
                
            except Exception as e:
                error = f"AI Error: {str(e)}"

    return render(request, 'index.html', {'results': results, 'error': error})

# Update your analyze function to accept the extra parameter
def analyze_resume_ai(resume_text, job_description):
    """Calls Gemini with the Resume and the specific Job Description."""
    prompt = f"""
    You are an expert Recruitment Consultant and ATS Optimizer.
    
    TASK:
    Evaluate the provided Resume specifically against the following Job Description/Domain.
    
    TARGET JOB DESCRIPTION:
    {job_description}
    
    RESUME TEXT:
    {resume_text}

    EVALUATION RUBRIC:
    - Role Alignment: How well does the experience match the JD requirements? (30)
    - Skill Match: Are the required technical/soft skills present? (30)
    - Experience Depth: Does the candidate have the right level of seniority? (20)
    - Keywords: Does the resume use industry-standard terminology for this specific role? (20)

    Return response in this EXACT format:
    Score: X/100
    Strengths:
    - [Specific to how they match the JD]
    Weaknesses:
    - [Missing skills or experiences required by the JD]
    Improvements:
    - [Specific keywords or metrics to add to better fit this specific role]
    """
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    return response.text