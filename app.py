import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Generative AI Document Q&A", page_icon="📄", layout="wide")

st.title("📄 Generative AI Document Q&A Assistant")
st.markdown("""
This assistant allows you to upload PDFs or Text documents and ask questions based strictly on the content of those documents.
It features concise answers, context-only responses, and source references.
""")

# Sidebar
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
if not api_key:
    st.sidebar.warning("Please enter your OpenAI API key to continue.")

st.sidebar.header("Document Upload")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs or Text files", type=["pdf", "txt"], accept_multiple_files=True
)

# Application State
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def process_documents(files):
    documents = []
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        try:
            if file.name.endswith(".pdf"):
                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()
            elif file.name.endswith(".txt"):
                loader = TextLoader(temp_file_path, encoding="utf-8")
                docs = loader.load()
            
            # Add the source filename to the document metadata for referencing
            for doc in docs:
                doc.metadata['source_file'] = file.name
                
            documents.extend(docs)
        finally:
            os.remove(temp_file_path)
            
    return documents

if st.sidebar.button("Process Documents"):
    if not api_key:
        st.sidebar.error("Please provide an OpenAI API key.")
    elif not uploaded_files:
        st.sidebar.error("Please upload at least one document.")
    else:
        with st.spinner("Processing documents..."):
            os.environ["OPENAI_API_KEY"] = api_key
            
            # 1. Extract Text
            docs = process_documents(uploaded_files)
            
            # 2. Split Content into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_documents(docs)
            
            # 3. Create Embeddings and Vector Store
            embeddings = OpenAIEmbeddings()
            vector_store = FAISS.from_documents(chunks, embeddings)
            st.session_state.vector_store = vector_store
            
            st.sidebar.success(f"Processed {len(docs)} documents into {len(chunks)} chunks.")

# Main Chat Interface
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Ask a question about your documents...")

if query:
    if not st.session_state.vector_store:
        st.warning("Please upload and process documents first.")
    elif not api_key:
        st.warning("Please enter your OpenAI API Key.")
    else:
        # Display user query
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.chat_history.append({"role": "user", "content": query})

        # Process response
        with st.chat_message("assistant"):
            with st.spinner("Searching and thinking..."):
                os.environ["OPENAI_API_KEY"] = api_key
                
                # Setup LLM
                llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
                
                # 4. Prompt rules for concise answers, context-only responses, and source-style references
                prompt_template = """
                You are a highly helpful, concise, and precise document assistant.
                Use ONLY the following pieces of retrieved context to answer the user's question.
                If the answer is not contained within the context, explicitly state: "I don't know based on the provided context." Do not guess or use outside knowledge.
                Keep your answer extremely concise and to the point.
                Whenever you provide facts or information, you MUST include source-style references at the end of the relevant sentence or paragraph based on the metadata provided (e.g., [Source: filename.pdf]).

                Context:
                {context}

                Question:
                {input}

                Answer:
                """
                
                prompt = ChatPromptTemplate.from_template(prompt_template)
                
                # 5. Retrieve and Answer
                retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 4})
                
                document_chain = create_stuff_documents_chain(llm, prompt)
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                
                # Execute the chain
                response = retrieval_chain.invoke({"input": query})
                answer = response["answer"]
                
                st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
