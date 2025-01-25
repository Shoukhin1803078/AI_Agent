

# import streamlit as st
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.schema.output_parser import StrOutputParser
# from langchain.schema.runnable import RunnablePassthrough
# import tempfile
# import os

# def render_rag_section():
#     st.markdown("""
#         <style>
#         .stTitle {
#             background: linear-gradient(120deg, #20bf55, #01baef);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#             font-size: 2.5em;
#             font-weight: 800;
#             animation: glow 2s ease-in-out infinite;
#         }
        
#         .step-container {
#             background: rgba(255,255,255,0.1);
#             border-radius: 10px;
#             padding: 15px;
#             margin: 10px 0;
#             border: 1px solid rgba(255,255,255,0.2);
#             animation: fadeIn 0.5s ease-out;
#         }
        
#         @keyframes glow {
#             0% { text-shadow: 0 0 10px rgba(32,191,85,0.5); }
#             50% { text-shadow: 0 0 20px rgba(1,186,239,0.5); }
#             100% { text-shadow: 0 0 10px rgba(32,191,85,0.5); }
#         }
        
#         @keyframes fadeIn {
#             from { opacity: 0; transform: translateY(-10px); }
#             to { opacity: 1; transform: translateY(0); }
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<p class="stTitle">📚 RAG with Chain</p>', unsafe_allow_html=True)

#     uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
#     api_key = st.session_state.get('api_key')

#     if uploaded_file and api_key:
#         os.environ["OPENAI_API_KEY"] = api_key
        
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#             tmp_file.write(uploaded_file.getvalue())
#             file_path = tmp_file.name

#         with st.spinner("Processing document..."):
#             loader = PyPDFLoader(file_path)
#             documents = loader.load()
#             text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=100)
#             texts = text_splitter.split_documents(documents)
            
#             embeddings = OpenAIEmbeddings()
#             vectorstore = FAISS.from_documents(texts, embeddings)
#             retriever = vectorstore.as_retriever()

#             template = """Answer the question based only on the following context:
#             {context}
#             Question: {question}
#             Answer: """
#             prompt = ChatPromptTemplate.from_template(template)

#             st.session_state.retriever = retriever
#             st.session_state.prompt = prompt
#             st.session_state.llm = llm = ChatOpenAI(temperature=0)
#             st.session_state.output_parser = output_parser = StrOutputParser()

#             chain = (
#                 {"context": retriever, "question": RunnablePassthrough()} 
#                 | prompt 
#                 | llm 
#                 | output_parser
#             )

#             st.session_state.chain = chain
#             st.success("Document processed! You can now ask questions.")

#         os.unlink(file_path)

#     if "chain" in st.session_state:
#         st.markdown("""
#         <div class="step-container">
#         <b>Chain Flow:</b><br>
#         Input → Retriever → Prompt → LLM → Output Parser → Answer
#         </div>
#         """, unsafe_allow_html=True)
        
#         question = st.text_input("Ask a question about your document:")
#         if question:
#             with st.spinner("Processing..."):
#                 response = st.session_state.chain.invoke(question)
                
#                 with st.expander("View Answer", expanded=True):
#                     st.write(response)

#                 with st.expander("View Chain Steps"):
#                     cols = st.columns(5)
#                     for i, step in enumerate(["Question", "Context", "Prompt", "LLM Response", "Final"]):
#                         with cols[i]:
#                             st.markdown(f"**{i+1}. {step}**")
                    
#                     retrieved_docs = st.session_state.retriever.invoke(question)
#                     prompt_value = st.session_state.prompt.format(
#                         context=retrieved_docs[0].page_content,
#                         question=question
#                     )
#                     llm_response = st.session_state.llm.invoke(prompt_value)
                    
#                     st.info(question)
#                     for i, doc in enumerate(retrieved_docs):
#                         st.code(doc.page_content, language="text")
#                     st.code(prompt_value, language="text")
#                     st.code(llm_response.content, language="text")
#                     st.success(response)


# --------------------------------------------------------------







































# import streamlit as st
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.schema.output_parser import StrOutputParser
# from langchain.schema.runnable import RunnablePassthrough
# import tempfile
# import os
# def render_rag_section():
#    if 'messages' not in st.session_state:
#        st.session_state.messages = []

#    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
#    api_key = st.session_state.get('api_key')

#    if uploaded_file and api_key:
#        os.environ["OPENAI_API_KEY"] = api_key
       
#        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#            tmp_file.write(uploaded_file.getvalue())
#            file_path = tmp_file.name

#        with st.spinner("Processing document..."):
#            loader = PyPDFLoader(file_path)
#            documents = loader.load()
#            text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=100)
#            texts = text_splitter.split_documents(documents)
           
#            embeddings = OpenAIEmbeddings(openai_api_key=api_key)
#            vectorstore = FAISS.from_documents(texts, embeddings)
#            retriever = vectorstore.as_retriever()

#            template = """Answer the question based on the context: {context}\nQuestion: {question}\nAnswer:"""
#            prompt = ChatPromptTemplate.from_template(template)

#            st.session_state.chain = (
#                {"context": retriever, "question": RunnablePassthrough()} 
#                | prompt 
#                | ChatOpenAI(api_key=api_key, temperature=0) 
#                | StrOutputParser()
#            )
#            st.success("Document processed! Ask questions below.")

#        os.unlink(file_path)

#    if "chain" in st.session_state:
#        chat_container = st.container()
#        chat_container.markdown("---")
       
#        for message in st.session_state.messages:
#            with chat_container:
#                col1, col2 = st.columns([1, 12])
#                with col1:
#                    st.write("👤" if message["role"] == "user" else "🤖")
#                with col2:
#                    st.write(message["content"])
#                st.markdown("---")

#        question = st.text_input("Ask a question:", placeholder="Type your question here...")
#        if st.button("Send", use_container_width=True):
#            if question:
#                st.session_state.messages.append({"role": "user", "content": question})
#                with st.spinner("Thinking..."):
#                    response = st.session_state.chain.invoke(question)
#                    st.session_state.messages.append({"role": "assistant", "content": response})
#                st.rerun()
























from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import tempfile
import os
import streamlit as st

def process_document(uploaded_file, api_key, api_type='openai'):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        file_path = tmp_file.name

    with st.spinner("Processing document..."):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        
        if api_type == 'openai':
            os.environ["OPENAI_API_KEY"] = api_key
            embeddings = OpenAIEmbeddings(openai_api_key=api_key)
            llm = ChatOpenAI(api_key=api_key, temperature=0)
        else:
            os.environ["GROQ_API_KEY"] = api_key
            embeddings = HuggingFaceEmbeddings()
            llm = ChatGroq(
                api_key=api_key,
                model="mixtral-8x7b-32768",  # Updated model
                temperature=0
            )

        vectorstore = FAISS.from_documents(texts, embeddings)
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            verbose=True
        )
        
        st.session_state.chain = chain
        st.success("Document processed! Start chatting below.")

    os.unlink(file_path)



def render_rag_section():
   st.title("📚 Document Chatbot")

   if "chat_history" not in st.session_state:
       st.session_state.chat_history = []

   # Document upload section
   upload_container = st.container()
   with upload_container:
       uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
       api_key = st.session_state.get('api_key')
       api_type = st.session_state.get('active_api')

       if uploaded_file and api_key:
           if "chain" not in st.session_state:
               process_document(uploaded_file, api_key, api_type)
               st.success("Document processed! Start chatting below.")

   # Chat section
   chat_container = st.container()
   input_container = st.container()

   with chat_container:
       st.markdown('<div style="height: 400px; overflow-y: auto;">', unsafe_allow_html=True)
       for message in st.session_state.chat_history:
           with st.chat_message(message["role"]):
               st.markdown(message["content"])
       st.markdown('</div>', unsafe_allow_html=True)

   with input_container:
       st.markdown('<div style="position: fixed; bottom: 0; width: 100%; background-color: white; padding: 10px;">', unsafe_allow_html=True)
       if prompt := st.chat_input("Ask a question..."):
           st.session_state.chat_history.append({"role": "user", "content": prompt})
           
           with chat_container:
               with st.chat_message("user"):
                   st.markdown(prompt)

               with st.chat_message("assistant"):
                   with st.spinner("Thinking..."):
                       response = st.session_state.chain.invoke({"question": prompt})
                       st.markdown(response["answer"])
                       st.session_state.chat_history.append({
                           "role": "assistant", 
                           "content": response["answer"]
                       })
       st.markdown('</div>', unsafe_allow_html=True)