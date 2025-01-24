


# import streamlit as st

# def render_sidebar():
#     with st.sidebar:
#         st.title("Settings")
#         api_key = st.text_input("OpenAI API Key", type="password")
#         return api_key




# ----------------------------version2-----------------------
import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("Settings")
        
        if 'active_api' not in st.session_state:
            st.session_state.active_api = None
            
        openai_key = st.text_input("OpenAI API Key", type="password")
        groq_key = st.text_input("Groq API Key", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Activate OpenAI"):
                st.session_state.active_api = 'openai'
                st.session_state.api_key = openai_key
                
        with col2:
            if st.button("Activate Groq"):
                st.session_state.active_api = 'groq'
                st.session_state.api_key = groq_key
                
        if st.session_state.active_api:
            st.success(f"{st.session_state.active_api.title()} API Active")
            
        return st.session_state.get('api_key')