# components/rag_using_groq/rag_groq.py
import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def setup_vectorstore():
   persist_directory = "components/rag_using_groq/vector_db_dir"
   embeddings = HuggingFaceEmbeddings()
   vectorstore = Chroma(persist_directory=persist_directory,
                       embedding_function=embeddings)
   return vectorstore

def chat_chain(vectorstore):
   llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
   retriever = vectorstore.as_retriever()
   memory = ConversationBufferMemory(
       output_key="answer",
       memory_key="chat_history",
       return_messages=True
   )
   chain = ConversationalRetrievalChain.from_llm(
       llm=llm,
       retriever=retriever,
       memory=memory,
       return_source_documents=True
   )
   return chain

def render_rag_groq_section():
   if "chat_history" not in st.session_state:
       st.session_state.chat_history = []

   if "vectorstore" not in st.session_state:
       st.session_state.vectorstore = setup_vectorstore()

   if "conversational_chain" not in st.session_state:
       st.session_state.conversational_chain = chat_chain(st.session_state.vectorstore)

   chat_container = st.container()
   with chat_container:
       st.markdown('<div style="height: 600px; overflow-y: auto;">', unsafe_allow_html=True)
       for message in st.session_state.chat_history:
           with st.chat_message(message["role"]):
               st.markdown(message["content"])
       st.markdown('</div>', unsafe_allow_html=True)

   with st.container():
       st.markdown('<div style="position: fixed; bottom: 0; width: 100%; background-color: white; padding: 20px;">', unsafe_allow_html=True)
       if prompt := st.chat_input("Ask about the documents..."):
           st.session_state.chat_history.append({"role": "user", "content": prompt})
           with chat_container:
               with st.chat_message("user"):
                   st.markdown(prompt)
               with st.chat_message("assistant"):
                   response = st.session_state.conversational_chain.invoke({"question": prompt})
                   st.markdown(response["answer"])
                   st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})
       st.markdown('</div>', unsafe_allow_html=True)