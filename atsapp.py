#from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai
#load_dotenv()

#api_key = os.getenv("GOOGLE_API_KEY")

#genai.configure(api_key=api_key)
# Configure API key (better to use st.secrets or environment variables)

api_key = st.secrets["GOOGLE_API_KEY"]
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = api_key
genai.configure(api_key=api_key)

def get_gemini_response(input_text, pdf_content, prompt):
    """Get response from Gemini model"""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")  # Updated model name
        response = model.generate_content([prompt, pdf_content[0], input_text])
        return response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        return f"Error generating response: {str(e)}"

def input_pdf_setup(uploaded_file):
    """Convert PDF to image format for Gemini"""
    if uploaded_file is not None:
        try:
            images = pdf2image.convert_from_bytes(uploaded_file.read())
            first_page = images[0]
            
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            pdf_parts = [{
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }]
            return pdf_parts
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return None
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App Configuration
st.set_page_config(
    page_title="Shashwata's ATS Resume Expert", 
    page_icon="🎯", 
    layout="wide"
)

# Main header
st.header("🎯 ExpertResumeCheckv1.0" \
"")

# Input section
col1, col2 = st.columns([2, 1])

with col1:
    input_text = st.text_area(
        "Job Description (Optional)", 
        placeholder="Paste the job description here for better analysis...",
        height=150
    )

with col2:
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)", 
        type=["pdf"],
        help="Upload your resume in PDF format for ATS analysis"
    )

# File upload status
if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")
    st.info(f"File: {uploaded_file.name}")

# Action buttons
st.markdown("### Choose an analysis type:")
col1, col2, col3 = st.columns(3)

with col1:
    submit1 = st.button("📋 Analyze My Resume", use_container_width=True)

with col2:
    submit2 = st.button("🚀 Skill Improvement Tips", use_container_width=True)

with col3:
    submit3 = st.button("🎯 ATS Score and Match Percentage", use_container_width=True)

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager specializing in recruiting for Metallurgical and Materials Engineering roles in industries such as steel, mining, automotive, aerospace, and manufacturing.

Your task is to review the provided resume and provide a comprehensive evaluation covering:

Overall resume structure and formatting  clarity, readability, ATS compatibility.

Professional summary effectiveness  does it highlight expertise in metallurgy, materials science, or process engineering?

Skills and technical competencies  metallurgical testing (tensile, hardness, impact), heat treatment, failure analysis, corrosion testing, microscopy (SEM/EDS), welding, foundry operations, computational tools (ANSYS, Thermo-Calc, MATLAB, Python, etc.).

Work / project / internship experience relevance  link to metallurgical processes such as casting, rolling, forging, heat treatment, corrosion prevention, alloy design, or process optimization.

Education and certifications  metallurgy/materials science degree relevance, specialized training (NDT Level II, Six Sigma, Lean Manufacturing, corrosion engineering, welding certifications).

Areas for improvement  missing technical keywords, weak descriptions of projects, lack of quantified achievements.

ATS-friendly recommendations  how to optimize for roles such as:

Process Engineer (Metals & Alloys)

Quality & Failure Analysis Engineer

Corrosion / Materials Engineer

R&D Engineer in Metallurgy / Materials

Production / Operations Engineer in Steel, Mining, or Aerospace

Provide specific, actionable feedback to help the candidate align their resume with metallurgical engineering job requirements and increase ATS success.
"""

input_prompt2 = """
🏭 Metallurgical Engineer Skill Improvement Prompt

You are a career development expert specializing in Metallurgical and Materials Engineering roles across industries such as steel, mining, aerospace, automotive, and advanced materials. Analyze the provided resume and suggest specific skill improvements to enhance employability and career growth.

Focus on:

Technical skills to add or strengthen  e.g., metallurgical testing (tensile, hardness, fatigue, impact), heat treatment, welding & joining, foundry processes, failure analysis, corrosion prevention, microscopy (SEM, TEM, XRD), computational tools (Thermo-Calc, JMatPro, ANSYS, Python, MATLAB).

Soft skills development opportunities  communication, technical report writing, project management, leadership in cross-functional engineering teams.

Certifications that would add value  e.g., NDT Level II/III, Six Sigma, Lean Manufacturing, AWS Welding Certification, Corrosion Engineering Certifications (NACE), Quality Management (ISO 9001/14001).

Industry-specific trending skills  additive manufacturing (3D printing metals), advanced alloys, sustainable metallurgy, AI/ML in materials design, Industry 4.0 in steel plants, automation in metallurgical processes.

Skills gap analysis  identify missing or underdeveloped skills compared to current industry expectations in process engineering, quality control, R&D, and failure analysis.

Learning path recommendations  structured roadmap (online courses, hands-on training, internships, certifications) to bridge identified gaps and advance career opportunities in metallurgy and materials science.

Provide practical, actionable advice tailored to metallurgical engineering roles, ensuring suggestions are aligned with ATS-friendly skills and market demands.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with deep understanding of resume parsing and keyword matching.

Analyze the resume against the provided job description and provide:

1. **ATS MATCH PERCENTAGE**: X%
2. **ATS SCORE**: X/100 (calculated based on keyword relevance, skills match, and formatting)
3. **KEYWORD ANALYSIS**:
   - Keywords Found: [list matching keywords]
   - Missing Keywords: [list important missing keywords]
4. **ATS OPTIMIZATION RECOMMENDATIONS**:
   - Formatting improvements
   - Keyword placement suggestions
   - Section organization tips
5. **FINAL ASSESSMENT**: Overall ATS compatibility and next steps

If no job description is provided, analyze the resume for general ATS compatibility, assign an ATS SCORE, and suggest improvements.
Focus on ensuring the resume is well-structured, uses relevant industry keywords, and follows best practices for ATS readability.
Dissect it properly and provide a detailed report.Give less ats score if the resume is not in proper format or lacks keywords.
"""

# Handle button clicks
if submit1:
    if uploaded_file is not None:
        with st.spinner("Analyzing your resume..."):
            pdf_content = input_pdf_setup(uploaded_file)
            if pdf_content:
                response = get_gemini_response(input_text, pdf_content, input_prompt1)
                st.subheader("📋 Resume Analysis Report")
                st.markdown(response)
    else:
        st.error("❌ Please upload a PDF file to get started.")

elif submit2:
    if uploaded_file is not None:
        with st.spinner("Generating skill improvement recommendations..."):
            pdf_content = input_pdf_setup(uploaded_file)
            if pdf_content:
                response = get_gemini_response(input_text, pdf_content, input_prompt2)
                st.subheader("🚀 Skill Development Recommendations")
                st.markdown(response)
    else:
        st.error("❌ Please upload a PDF file to get started.")

elif submit3:
    if uploaded_file is not None:
        if not input_text.strip():
            st.warning("⚠️ For accurate ATS matching, please provide a job description in the text area above.")
        
        with st.spinner("Calculating ATS match percentage..."):
            pdf_content = input_pdf_setup(uploaded_file)
            if pdf_content:
                response = get_gemini_response(input_text, pdf_content, input_prompt3)
                st.subheader("🎯 ATS Compatibility Analysis")
                st.markdown(response)
    else:
        st.error("❌ Please upload a PDF file to get started.")

# Footer
st.markdown("---")
st.markdown("💡 **Tips**: For best results, upload a clean PDF resume and provide a detailed job description for ATS matching.")
st.markdown("🔒 **Privacy**: Your resume is processed securely and not stored permanently.")