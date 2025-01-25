
# components/job_agent.py
import streamlit as st
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from openai import OpenAI
from groq import Groq

def create_job_agent(api_key):
   return Agent(
       name="Job Search Agent",
       role="Search jobs based on user profile",
       model=OpenAIChat(api_key=api_key),
       tools=[DuckDuckGo()],
       instructions=[
           "Search for jobs matching user skills and experience",
           "Include both Bangladesh and worldwide opportunities", 
           "Return at least 10 relevant job links",
           "Format results clearly"
       ],
       show_tool_calls=True,
       markdown=True
   )

def search_jobs_from_summary(summary, api_key):
   job_agent = Agent(
       name="Job Search Agent",
       role="Find relevant jobs based on CV summary",
       model=OpenAIChat(api_key=api_key),
       tools=[DuckDuckGo()],
       instructions=[
           "Search for jobs matching the CV summary",
           "Include both local and worldwide opportunities",
           "Organize jobs by role/category",
           "Include job links and brief descriptions",
           "List at least 5-10 relevant positions"
       ],
       show_tool_calls=True,
       markdown=True
   )

   query = f"Find relevant job opportunities based on this CV summary:\n{summary}"
   print(f"query ==========> {query}")
   x = job_agent.run(query)
   print(f" job========= {x}")
   return x
#    return job_agent.run(query)

def search_jobs(agent, skills, experience, interests):
   query = f"""Find jobs matching:
   Skills: {skills}
   Experience: {experience} 
   Interests: {interests}
   Include both Bangladesh and worldwide opportunities."""
   
   return agent.run(query)

def analyze_summary_cv(text, api_key, api_type='openai'):
   prompt = f"Please provide a concise summary of this CV analysis, focusing on key skills, experience, and strengths:\n\n{text}"
   
   if api_type == 'openai':
       client = OpenAI(api_key=api_key)
       response = client.chat.completions.create(
           model="gpt-4",
           messages=[
               {"role": "system", "content": "You are a professional CV analyzer. Provide concise summaries."},
               {"role": "user", "content": prompt}
           ]
       )
       return response.choices[0].message.content
   else:
       client = Groq(api_key=api_key)
       response = client.chat.completions.create(
           model="llama-3.3-70b-versatile",
           messages=[
               {"role": "system", "content": "You are a professional CV analyzer. Provide concise summaries."},
               {"role": "user", "content": prompt}
           ]
       )
       return response.choices[0].message.content

def render_job_section():
   st.header("Job Search")
   
   if 'summary_result' not in st.session_state:
       st.session_state.summary_result = ""
   if 'job_matches' not in st.session_state:
       st.session_state.job_matches = ""

#    if st.session_state.get('show_raw_content') and st.session_state.get('cv_text'):
#        st.subheader("Your CV Content")
#        st.text_area("CV Content", st.session_state.cv_text, height=200, key="job_cv_content")
       
   if st.session_state.get('analysis_result'):
    #    st.subheader("Your CV Analysis")
    #    st.write(st.session_state.analysis_result)

       analyze_button = st.button("Analyze CV summary")
       if analyze_button:
           api_key = st.session_state.get('api_key')
           if not api_key:
               st.error("Please enter and activate an API key in sidebar")
           else:
               with st.spinner('Analyzing your CV summary...'):
                   st.session_state.summary_result = analyze_summary_cv(
                       st.session_state.analysis_result,
                       api_key,
                       st.session_state.active_api
                   )
                   
   if st.session_state.get('summary_result'):
       st.subheader("CV Summary")
       st.write(st.session_state.summary_result)
       
       if st.button("Find Matching Jobs Based on CV"):
           api_key = st.session_state.get('api_key')
           if not api_key:
               st.error("Please enter and activate an API key in sidebar")
           else:
               with st.spinner('Searching relevant jobs...'):
                   st.session_state.job_matches = search_jobs_from_summary(
                       st.session_state.summary_result,
                       api_key
                   )
   
   if st.session_state.get('job_matches'):
       st.subheader("Matching Jobs Based on Your CV")
       st.write(st.session_state.job_matches)

#    if st.session_state.get('improvement_result'):
#        st.subheader("Suggested CV Improvements")
#        st.write(st.session_state.improvement_result)
   







#    st.header("Search Jobs Based on Your Profile")
#    skills = st.text_area("Skills", key="skills_input")
#    experience = st.text_area("Experience", key="experience_input")
#    interests = st.text_area("Interests", key="interests_input")
   
#    if st.button("Search Jobs"):
#        api_key = st.session_state.get('api_key')
#        if not api_key:
#            st.error("Please enter and activate an API key in sidebar")
#            return
           
#        agent = create_job_agent(api_key)
#        results = search_jobs(agent, skills, experience, interests)
#        st.write(results)





















