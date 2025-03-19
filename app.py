import streamlit as st
import openai
import pdfplumber
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=openai.api_key)
model = 'gpt-3.5-turbo'
# Function to extract text from PDF resume
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

# Function to extract keywords from Job Description using OpenAI API
def extract_keywords(job_desc):
    prompt = f"Extract key skills, qualifications, and experience from the following job description:\n\n{job_desc}"
    
    

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# Function to score resume based on Job Description
def score_resume(job_desc, resume_text):
    prompt = f"""
    Compare the following resume with the job description and score it out of 10. 
    Provide a breakdown of why the resume received this score.

    Job Description:
    {job_desc}

    Resume:
    {resume_text}

    Output should be in this format: 
    Score: X/10
    Breakdown:
    - Skill Match: X/10
    - Experience Match: X/10
    - Education Match: X/10
    - Recommendations: [Provide 2-3 suggestions to improve]
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content  

# Streamlit UI
st.title("🔍 AI Resume Analyzer")

# Job description input
st.subheader("📄 Paste Job Description")
job_description = st.text_area("Enter the job description here...")

# Resume PDF Upload
st.subheader("📂 Upload Your Resume (PDF)")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if st.button("Analyze Resume"):
    if job_description and uploaded_file:
        # Extract text from resume
        resume_text = extract_text_from_pdf(uploaded_file)
        
        # Get keywords from job description
        st.subheader("🔑 Extracted Job Keywords")
        keywords = extract_keywords(job_description)
        st.write(keywords)
        
        # Score Resume
        st.subheader("📊 Resume Score & Analysis")
        score_analysis = score_resume(job_description, resume_text)
        st.write(score_analysis)

    else:
        st.error("⚠️ Please provide both a job description and upload a resume!")
