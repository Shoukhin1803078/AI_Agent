
import streamlit as st
from PyPDF2 import PdfReader
import docx
from openai import OpenAI
from groq import Groq

def read_pdf(file):
   pdf = PdfReader(file)
   return "".join(page.extract_text() for page in pdf.pages)

def read_docx(file):
   doc = docx.Document(file)
   return "\n".join(para.text for para in doc.paragraphs)

def analyze_with_groq(text, api_key):
   client = Groq(api_key=api_key)
   response = client.chat.completions.create(
       model="llama-3.3-70b-versatile",
       messages=[
           {"role": "system", "content": "Analyze this CV and provide insights."},
           {"role": "user", "content": text}
       ]
   )
   return response.choices[0].message.content

def analyze_cv(text, api_key, api_type='openai'):
   if api_type == 'openai':
       client = OpenAI(api_key=api_key)
       response = client.chat.completions.create(
           model="gpt-4",
           messages=[
               {"role": "system", "content": "Analyze this CV and provide insights."},
               {"role": "user", "content": text}
           ]
       )
       return response.choices[0].message.content
   else:
       return analyze_with_groq(text, api_key)

def get_cv_improvements(text, api_key, api_type='openai'):
   if api_type == 'openai':
       client = OpenAI(api_key=api_key)
       response = client.chat.completions.create(
           model="gpt-4",
           messages=[
               {"role": "system", "content": "Suggest improvements for this CV."},
               {"role": "user", "content": text}
           ]
       )
       return response.choices[0].message.content
   else:
       return analyze_with_groq(text, api_key)

def render_cv_section():
   st.markdown("""
       <style>
       .css-1kyxreq {
           background: linear-gradient(90deg, #2b5876, #4e4376);
           -webkit-background-clip: text;
           -webkit-text-fill-color: transparent;
           font-size: 2.5em;
           margin-bottom: 30px;
           animation: fadeIn 1s ease-in;
       }
       
       .stFileUploader {
           border: 2px dashed #4e4376;
           border-radius: 10px;
           padding: 20px;
           transition: all 0.3s ease;
           background: rgba(255, 255, 255, 0.9);
       }
       
       .stFileUploader:hover {
           border-color: #2b5876;
           box-shadow: 0 5px 15px rgba(43, 88, 118, 0.2);
           transform: translateY(-2px);
       }
       
       .stButton>button {
           background: linear-gradient(45deg, #2b5876, #4e4376);
           color: white;
           border: none;
           padding: 12px 24px;
           border-radius: 25px;
           font-weight: 600;
           transition: all 0.3s ease;
           transform: scale(1);
           box-shadow: 0 4px 15px rgba(0,0,0,0.1);
           width: 100%;
           max-width: 300px;
           margin: 10px auto;
           display: block;
       }
       
       .stButton>button:hover {
           transform: scale(1.05);
           box-shadow: 0 7px 20px rgba(0,0,0,0.2);
           background: linear-gradient(45deg, #4e4376, #2b5876);
       }
       
       .stTextArea>div>div {
           border-radius: 10px;
           border: 1px solid #4e4376;
           box-shadow: 0 2px 10px rgba(0,0,0,0.05);
           background: white;
       }
       
       .stSubheader {
           color: #2b5876;
           font-weight: 600;
           border-left: 4px solid #4e4376;
           padding-left: 10px;
           margin: 20px 0;
           background: linear-gradient(90deg, rgba(43,88,118,0.1) 0%, rgba(255,255,255,0) 100%);
       }
       
       .stAlert {
           animation: shake 0.5s ease-in-out;
           border-radius: 10px;
           border: none;
           background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
           color: white;
       }

       @keyframes shake {
           0%, 100% { transform: translateX(0); }
           25% { transform: translateX(-5px); }
           75% { transform: translateX(5px); }
       }
       
       @keyframes fadeIn {
           from { opacity: 0; transform: translateY(-20px); }
           to { opacity: 1; transform: translateY(0); }
       }
       
       .st-emotion-cache-1y4p8pa {
           padding: 1rem;
           border-radius: 10px;
           background: white;
           box-shadow: 0 4px 15px rgba(0,0,0,0.1);
           margin: 10px 0;
           animation: slideIn 0.5s ease-out;
       }

       @keyframes slideIn {
           from { opacity: 0; transform: translateX(-20px); }
           to { opacity: 1; transform: translateX(0); }
       }
       </style>
   """, unsafe_allow_html=True)

   st.header("CV Analysis")
   
   for state in ['cv_text', 'analysis_result', 'improvement_result', 'show_raw_content']:
       if state not in st.session_state:
           st.session_state[state] = "" if state != 'show_raw_content' else False

   uploaded_file = st.file_uploader("Upload your CV", type=['pdf', 'docx'])
   
   if uploaded_file:
       st.session_state.cv_text = read_pdf(uploaded_file) if uploaded_file.type == "application/pdf" else read_docx(uploaded_file)
   
   if st.button("Get cv raw content") and st.session_state.cv_text:
       st.session_state.show_raw_content = True
       
   if st.session_state.show_raw_content and st.session_state.cv_text:
       st.text_area("CV Content", st.session_state.cv_text, height=200)

   analyze_button = st.button("Analyze CV")
   if analyze_button and st.session_state.cv_text:
       api_key = st.session_state.get('api_key')
       if not api_key:
           st.error("Please enter and activate an API key in sidebar")
       else:    
           with st.spinner('Analyzing your CV...'):
               st.session_state.analysis_result = analyze_cv(
                   st.session_state.cv_text, 
                   api_key, 
                   st.session_state.active_api
               )
   
   if st.session_state.analysis_result:
       st.subheader("Analysis")
       st.write(st.session_state.analysis_result)

   improve_button = st.button("Get improvement from OpenAI")
   if improve_button and st.session_state.cv_text:
       api_key = st.session_state.get('api_key')
       if not api_key:
           st.error("Please enter and activate an API key in sidebar")
       else:
           with st.spinner('Generating improvements...'):
               st.session_state.improvement_result = get_cv_improvements(
                   st.session_state.cv_text,
                   api_key,
                   st.session_state.active_api
               )
   
   if st.session_state.improvement_result:
       st.subheader("Suggested Improvements")
       st.write(st.session_state.improvement_result)