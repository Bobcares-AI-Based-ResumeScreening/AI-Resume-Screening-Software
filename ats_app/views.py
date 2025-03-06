from django.shortcuts import render
from .forms import ResumeForm
import fitz
from sentence_transformers import SentenceTransformer, util
import spacy
import numpy as np
import re

nlp = spacy.load("en_core_web_sm")

model = SentenceTransformer('all-mpnet-base-v2')

JOB_DESCRIPTION = """
We are looking for a Software Engineer with 5+ years of experience in Python development, machine learning, and cloud computing. Passionate about building scalable applications and solving complex problems with AI.
"""

def extract_resume_text(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = "\n".join([page.get_text("text") for page in doc])
        text = clean_text(text)
        return text
    except Exception as e:
        return str(e)


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip().lower()

def calculate_similarity(resume_text, job_desc):
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_desc, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
    
    return similarity * 100


def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = {token.lemma_ for token in doc if token.is_alpha and not token.is_stop}
    return keywords


def normalize_keyword_score(resume_text, job_desc):
    job_keywords = extract_keywords(job_desc)
    resume_keywords = extract_keywords(resume_text)
    matched_keywords = job_keywords.intersection(resume_keywords)
    
    if not job_keywords:
        return 0

    return (len(matched_keywords) / len(job_keywords)) * 100


def ats_score(resume_text, job_desc):
    cosine_score = calculate_similarity(resume_text, job_desc)
    keyword_score = normalize_keyword_score(resume_text, job_desc)

    
    final_score = (cosine_score * 0.7) + (keyword_score * 0.3)
    
    return round(final_score, 2)


def upload_resume(request):
    score = None
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = request.FILES['resume']
            resume_text = extract_resume_text(resume_file)
            score = ats_score(resume_text, JOB_DESCRIPTION)
    else:
        form = ResumeForm()
    
    return render(request, 'ats_app/upload.html', {'form': form, 'score': score})
