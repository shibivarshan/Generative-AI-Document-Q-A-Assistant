# 📄 Generative AI Document Q&A Assistant

A robust, user-friendly web application that allows you to upload PDF and Text documents, and ask questions based strictly on the content of those documents. The assistant provides concise, context-aware answers along with source-style references.

Built with **Streamlit** for the frontend and **LangChain** for the AI orchestration.

## ✨ Features
- **Multi-Document Support**: Upload and process multiple `.pdf` or `.txt` files at once.
- **Smart Chunking**: Uses `RecursiveCharacterTextSplitter` to handle large documents efficiently.
- **High-Quality Embeddings**: Leverages OpenAI Embeddings with a local FAISS vector database for fast and precise context retrieval.
- **Strict Prompt Engineering**: Engineered to prevent hallucinations. The AI will only answer based on the provided document context and will explicitly state if the answer is not found.
- **Source References**: Automatically appends the source filename to the information it provides.
  
## 🏗️ System Architecture
PDF Document
      |
      ↓
Text Extraction
      |
      ↓
Text Chunking
      |
      ↓
Embedding Generation
      |
      ↓
FAISS Vector Database
      |
      ↓
Similarity Search
      |
      ↓
LLM Response Generation

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- An OpenAI API Key

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

### 3. Configuration
Set up your OpenAI API key. You can do this in two ways:
- **Environment Variable**: Rename `.env.example` to `.env` and paste your API key inside.
- **In-App**: You can simply run the app and paste the API key directly into the sidebar UI.

### 4. Run the Application
Start the Streamlit server:
```bash
python -m streamlit run app.py
```
The application will automatically open in your default web browser at `http://localhost:8501`.

## 🛠️ Technology Stack
- **UI Framework**: [Streamlit](https://streamlit.io/)
- **LLM Framework**: [LangChain](https://www.langchain.com/)
- **Vector Store**: [FAISS](https://github.com/facebookresearch/faiss)
- **AI Models**: OpenAI (`gpt-3.5-turbo`, `text-embedding-3-small`)

## 📂 Project Workflow
User uploads a document
Document content is extracted and processed
Text is divided into meaningful chunks
Embeddings are generated
Vector search retrieves relevant information
LLM generates the final response

## 🎯 Use Cases

Document analysis
Knowledge assistants
Research support
Enterprise document search
Internal company Q&A systems

## 📌 Future Improvements

Multi-document conversation memory
Better document ranking
Cloud deployment
User authentication

## 👨‍💻 Author
Shibivarshan
Generative AI Engineer

## 📝 License
This project is open-source and available under the MIT License.

## output
<img width="1600" height="716" alt="Image" src="https://github.com/user-attachments/assets/e43d3465-378e-4d0b-b397-abbd36bb33f0" />
