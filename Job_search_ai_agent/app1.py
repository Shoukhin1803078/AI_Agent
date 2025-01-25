
import streamlit as st
from components.sidebar1 import render_sidebar
from components.cv_analyzer1 import render_cv_section
from components.job_agent1 import render_job_section
from components.rag.rag import render_rag_section
from components.rag_using_groq.rag_groq import render_rag_groq_section
def main():
#    st.set_page_config(layout="wide")
   
   st.markdown("""
       <style>
       /* Main title styling */
       .main-title {
           background: linear-gradient(120deg, #FF4B2B, #FF416C, #8E2DE2);
           -webkit-background-clip: text;
           -webkit-text-fill-color: transparent;
           font-size: 3.5em;
           font-weight: 800;
           text-align: center;
           padding: 20px;
           margin-bottom: 30px;
           text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
           animation: titleGlow 3s ease-in-out infinite;
       }

       @keyframes titleGlow {
           0% { transform: scale(1); }
           50% { transform: scale(1.02); filter: brightness(1.1); }
           100% { transform: scale(1); }
       }

       /* Tab styling */
       .stTabs [data-baseweb="tab-list"] {
           gap: 24px;
           background: linear-gradient(90deg, #141E30, #243B55);
           padding: 15px;
           border-radius: 15px;
           box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
       }

       .stTabs [data-baseweb="tab"] {
           height: 60px;
           padding: 10px 30px;
           background: rgba(255, 255, 255, 0.1);
           backdrop-filter: blur(4px);
           border-radius: 12px;
           transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
           border: 1px solid rgba(255, 255, 255, 0.18);
       }

       .stTabs [data-baseweb="tab"]:hover {
           transform: translateY(-3px) scale(1.05);
           box-shadow: 0 10px 20px rgba(0,0,0,0.2);
           background: rgba(255, 255, 255, 0.2);
       }

       .stTabs [data-baseweb="tab-list"] button p {
           font-size: 24px;
           font-weight: 700;
           background: linear-gradient(120deg, #00F260, #0575E6, #00F260);
           background-size: 200% auto;
           -webkit-background-clip: text;
           -webkit-text-fill-color: transparent;
           animation: shine 3s linear infinite;
       }

       @keyframes shine {
           to {
               background-position: 200% center;
           }
       }

       .stTabs [data-baseweb="tab"][aria-selected="true"] {
           background: rgba(255, 255, 255, 0.25);
           box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
           border: 1px solid rgba(255, 255, 255, 0.3);
           animation: pulse 2s infinite;
       }

       @keyframes pulse {
           0% { box-shadow: 0 0 0 0 rgba(255,255,255, 0.4); }
           70% { box-shadow: 0 0 0 10px rgba(255,255,255, 0); }
           100% { box-shadow: 0 0 0 0 rgba(255,255,255, 0); }
       }
       </style>""", unsafe_allow_html=True)
   
   st.markdown('<h1 class="main-title"> All In One Assistant</h1>', unsafe_allow_html=True)
   api_key = render_sidebar()
   
#    tab1, tab2, tab3 = st.tabs(["CV Analysis", "Job Search", "RAG"])
   tab1, tab2, tab3, tab4 = st.tabs(["CV Analysis", "Job Search", "RAG", "RAG using Groq"])
   with tab1:
       render_cv_section()
   with tab2:
       render_job_section()
   with tab3:
       render_rag_section()
   with tab4:
        render_rag_groq_section()

if __name__ == "__main__":
   main()