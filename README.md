# 🤖 Smart Recruiter – AI Resume Analyzer

An AI-powered resume analysis web application that uses the **Google Gemini API** to evaluate resumes, generate intelligent scores, identify strengths and weaknesses, and provide personalized feedback based on the user's selected job domain.

## ✨ Features

* 📄 **Resume PDF Analysis** – Upload and analyze resumes in PDF format.
* 🤖 **AI-Powered Evaluation** – Uses Google Gemini to understand and evaluate resume content.
* 📊 **Resume Scoring** – Generates an overall score based on resume quality and relevance.
* 💼 **Job Domain Selection** – Analyze resumes according to a specific career/job domain.
* 💪 **Strength Identification** – Highlights the strongest parts of the resume.
* ⚠️ **Weakness Detection** – Identifies areas that need improvement.
* 💡 **Personalized Recommendations** – Provides actionable suggestions to improve the resume.
* 🔐 **Authentication System** – Includes user login and registration functionality.
* 🗄️ **Database Integration** – Stores application and user-related data using SQLite.

## 🛠️ Tech Stack

* **Python**
* **Django**
* **Google Gemini API**
* **SQLite**
* **HTML / CSS**
* **JavaScript**

## 🔄 How It Works

```text
        👤 User
           │
           ▼
    📄 Upload Resume
           │
           ▼
   💼 Select Job Domain
           │
           ▼
     ⚙️ Django Backend
           │
           ▼
    🤖 Gemini AI Analysis
           │
           ▼
      📊 Resume Score
           │
     ┌─────┼─────┐
     ▼     ▼     ▼
 Strengths Weaknesses Recommendations
           │
           ▼
       📋 Results
```

## 🎯 Project Objective

The purpose of **Smart Recruiter** is to help job seekers understand how effectively their resume represents their skills and experience for a specific career domain.

Instead of manually reviewing a resume, users can upload their PDF and receive an AI-powered evaluation with a score, strengths, weaknesses, and improvement suggestions.

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/Smart-recruiter.git
cd Smart-recruiter
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Gemini API

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

> Never commit your API key or `.env` file to GitHub.

### Run Migrations

```bash
python manage.py migrate
```

### Start the Server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## 📈 Future Improvements

* 🎯 ATS compatibility analysis
* 📋 Resume vs. job-description matching
* ✍️ AI-powered resume improvement
* 📑 AI-generated resume templates
* 📊 Advanced resume analytics
* 🔍 Keyword and skill-gap detection
* 💼 Job recommendations based on resume
* 📈 Resume improvement tracking

## 👨‍💻 Author

**Ahmad Abbas**

Computer Science Student | AI & Backend Developer

---

⭐ **If you find this project useful, consider giving it a star!**
