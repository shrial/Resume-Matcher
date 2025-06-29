from flask import Flask, render_template , request #frm flask getting class Flask
from pdfminer.high_level import extract_text
import spacy # Importing spaCy for NLP tasks
from spacy.matcher import PhraseMatcher
import json
import requests

nlp = spacy.load("en_core_web_sm") # Load the spaCy model for English language processing

app = Flask(__name__) # Initialize the Flask application

# api work
url="https://remotive.com/api/remote-jobs?limit=5" # URL to fetch remote job data
response = requests.get(url)

@app.route('/') # basically like u enter the URL and the function is called
def index():
    return render_template('index.html') # This will render the index.html template

def get_skills(text, skill_list): # Function to extract skills from the resume text
    matcher = PhraseMatcher(nlp.vocab)
    patterns=[nlp.make_doc(skill) for skill in skill_list] # this is for the json file
    matcher.add("skills",patterns)
    
    #now resume text is processed
    doc=nlp(text)
    matches = matcher(doc)
    skills_found = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        skills_found.add(span.text.lower())
    return skills_found
    
    
@app.route('/upload', methods = ['POST'])
def upload():
    f=request.files['resume'] # Get the file from the request
    if request.method == 'POST':
        fn=f.filename.lower()
        text=extract_text(f.stream) 
        
        job_data = response.json()['jobs'] # Get the job data from the API response
        job_skills=[]
        
        for job in job_data:
            for key,skill in job.items():
                if key not in ['title','category','description']:
                    continue
                skill = skill.replace(',', ' ').replace('.', ' ').replace('(', ' ').replace(')', ' ')
                job_skills.extend(skill.split(' '))
        resume_skills = get_skills(text.lower(), job_skills)
         # Compare with jobs
        results = []
        for job in job_data:
            for key, values in job.items():
                if not isinstance(values, str):
                    continue
                match = set(val.lower() for val in values.split(' ')).intersection(resume_skills)
                if match:
                    results.append({
                        'title': job['title'],
                        'company': job['company_name'],
                        'type': job['job_type'],
                        'description': job['description'],
                        'url': job['url']
                        })
                    break
        return render_template("results.html", results=results)


    
if __name__ == '__main__': # Run the application
    app.run(debug=True) # Set debug=True for development mode
    # In production, you would set debug=False 
    
    
