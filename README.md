# Resume-Matcher
ResumeMatcher is a Flask-based web app that reads a PDF resume, extracts relevant skills and keywords using NLP (spaCy), and suggests remote jobs by matching those skills with live job postings from an API.

**Flow :**
- Upload a PDF resume
- Extract skills and keywords using spaCy + PhraseMatcher
- Fetch live remote jobs from Remotive API
- Match resume skills with job descriptions
- View suggested job listings with titles, companies, and descriptions

**Tech Stack Used :**
- Python
- Flask – for web framework
- spaCy – for natural language processing
- pdfminer – for extracting text from PDFs
- Requests – for calling the Remotive API
- HTML,CSS - for the frontend

API documentation link: https://github.com/remotive-com/remote-jobs-api 
