# import streamlit as st
# from components.sidebar import render_sidebar
# from components.cv_analyzer import render_cv_section
# from components.job_agent import render_job_section

# def main():
#     st.title("Job Search Assistant")
    
#     api_key = render_sidebar()
#     if api_key:
#         st.session_state['openai_api_key'] = api_key
    
#     tab1, tab2 = st.tabs(["CV Analysis", "Job Search"])
    
#     with tab1:
#         render_cv_section()
    
#     with tab2:
#         render_job_section()

# if __name__ == "__main__":
#     main()



# ------------------------version2-------------------
import streamlit as st
from components.sidebar import render_sidebar
from components.cv_analyzer import render_cv_section
from components.job_agent import render_job_section

def main():
    st.title("Job Search Assistant")
    api_key = render_sidebar()
    tab1, tab2 = st.tabs(["CV Analysis", "Job Search"])
    with tab1:
        render_cv_section()
    with tab2:
        render_job_section()

if __name__ == "__main__":
    main()
