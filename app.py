import streamlit as st
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
api_key = st.secrets("OPENAI_API_KEY")
# Setup OpenAI client
openai.api_key = api_key

# Helper function to extract text from PDF
def extract_text_from_pdf(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

# Streamlit app
st.set_page_config(page_title="Intelligent Resume Screener", page_icon="🧠")
st.title("🧠 Intelligent Resume Screener Bot")

# Upload Resume PDF
st.header("Step 1: Upload your Resume (PDF)")
resume_file = st.file_uploader("Choose your resume file", type=["pdf"])

# Upload Job Description PDF
st.header("Step 2: Upload the Job Description (PDF)")
jd_file = st.file_uploader("Choose the job description file", type=["pdf"])

# Analyze Button
if st.button("🚀 Analyze Resume vs JD"):
    if resume_file is not None and jd_file is not None:
        with st.spinner("Extracting and analyzing..."):
            # Extract text
            resume_text = extract_text_from_pdf(resume_file)
            jd_text = extract_text_from_pdf(jd_file)

            # Build system prompt
            prompt = f"""
You are an AI-powered Career Advisor and Resume Screening Assistant designed to simulate a top-level human recruiter.

Given the following:
- Resume Text
- Job Description Text

Perform the following steps:
1. Extract and list the top 10 key skills mentioned in the Resume.
2. Extract and list the top 10 key skills required in the Job Description.
3. Compare both lists and calculate a Match Score (in %).
4. Identify and list any missing important skills from the Resume compared to the JD.
5. Provide a friendly but professional feedback to the candidate:
   - Highlight strong points.
   - Suggest specific skills to add or learn.
   - Encourage improvement positively.

**Important Rules:**
- Be clear, concise, and professional in tone.
- Use bullet points and headings for easy readability.
- Match Score = (Number of Matching Skills / Total JD Skills) × 100
- If Resume is a perfect match, congratulate the candidate.
- If gaps exist, be motivating and suggest clear action points.

Respond in clean, easy-to-read Markdown style.

---

Resume:
{resume_text}

---

Job Description:
{jd_text}
            """

            # Call OpenAI
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=1500,
                )
                output = response['choices'][0]['message']['content']
                st.markdown(output)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error("Please upload both Resume and Job Description files before analyzing.")
