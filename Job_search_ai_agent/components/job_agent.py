
# # components/job_agent.py
# import streamlit as st
# from phi.agent import Agent
# from phi.model.openai import OpenAIChat
# from phi.tools.duckduckgo import DuckDuckGo

# def create_job_agent(api_key):
#     return Agent(
#         name="Job Search Agent",
#         role="Search jobs based on user profile",
#         model=OpenAIChat(api_key=api_key),
#         tools=[DuckDuckGo()],
#         instructions=[
#             "Search for jobs matching user skills and experience",
#             "Include both Bangladesh and worldwide opportunities",
#             "Return at least 10 relevant job links",
#             "Format results clearly"
#         ],
#         show_tool_calls=True,
#         markdown=True
#     )

# def search_jobs(agent, skills, experience, interests):
#     query = f"""Find jobs matching:
#     Skills: {skills}
#     Experience: {experience}
#     Interests: {interests}
#     Include both Bangladesh and worldwide opportunities."""
    
#     return agent.run(query)

# def render_job_section():
#     st.header("Job Search")
    
#     skills = st.text_area("Skills")
#     experience = st.text_area("Experience")
#     interests = st.text_area("Interests")
    
#     if st.button("Search Jobs"):
#         api_key = st.session_state.get('openai_api_key')
#         if not api_key:
#             st.error("Please enter OpenAI API key in sidebar")
#             return
            
#         agent = create_job_agent(api_key)
#         results = search_jobs(agent, skills, experience, interests)
#         st.write(results)




# components/job_agent.py
import streamlit as st
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo

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

def search_jobs(agent, skills, experience, interests):
    query = f"""Find jobs matching:
    Skills: {skills}
    Experience: {experience}
    Interests: {interests}
    Include both Bangladesh and worldwide opportunities."""
    
    return agent.run(query)

def render_job_section():
    st.header("Job Search")

    # Add unique keys to text areas
    if st.session_state.get('show_raw_content') and st.session_state.get('cv_text'):
        st.subheader("Your CV Content") 
        # st.text_area("CV Content", st.session_state.cv_text, height=200, key="job_cv_content")
        print(f"original-----==========> {st.session_state.cv_text}")

    if st.session_state.get('analysis_result'):
        st.subheader("Your CV Analysis")
        # st.write(st.session_state.analysis_result)
        print(f"cv analysis ==========> {st.session_state.analysis_result}")

    if st.session_state.get('improvement_result'):
        st.subheader("Suggested CV Improvements")
        # st.write(st.session_state.improvement_result)
        print(f"cv improvement ==========> {st.session_state.improvement_result}")
    
    st.header("Search Jobs Based on Your Profile")
    skills = st.text_area("Skills", key="skills_input")
    experience = st.text_area("Experience", key="experience_input") 
    interests = st.text_area("Interests", key="interests_input")
    
    if st.button("Search Jobs"):
        api_key = st.session_state.get('api_key')
        if not api_key:
            st.error("Please enter and activate an API key in sidebar")
            return
            
        agent = create_job_agent(api_key)
        results = search_jobs(agent, skills, experience, interests)
        st.write(results)