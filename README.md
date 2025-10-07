# RAG File Search System

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system that enables users to query files by their content and retrieve their file locations. Given a folder path, the system:

- Recursively reads all files from the folder
- Extracts text content and metadata (file name, full path)
- Creates vector embeddings of the content for semantic search
- Stores embeddings in a local vector store (ChromaDB)
- Accepts natural language queries (e.g., "Where is the Aadhaar card file?")
- Retrieves relevant documents and generates context-aware answers with Llama 3.2 or Hugging Face language models

## Features
- Text extraction from PDFs, DOCX, and images (via OCR)
- Embedding creation with Ollama GoogleEmbedding model or HuggingFace embeddings
- Local vector database using ChromaDB (offline support)
- Seamless integration with LLMs for precise question answering
- Efficient indexing and retrieval for large document collections

## Requirements
- Python 3.9 or higher
- Ollama for GoogleEmbedding model
- Llama 3.2 1B model (local or Ollama hosted)
- ChromaDB (installed locally)
- PyMuPDF, pdfplumber, python-docx, pytesseract for file text extraction
- LangChain (optional, for pipeline orchestration)

## Setup Instructions
1. Clone this repository  
2. Install dependencies:  
   `pip install -r requirements.txt`  
3. Install and start ChromaDB locally:  
   `pip install chromadb`  
   `chromadb run --path ./chroma_data`  
4. Configure Ollama and Llama 3.2 models (local or API)  
5. Provide folder path for indexing in config  

## Usage
- Run the indexing script to scan the folder, extract text, and index content  
- Launch query interface (CLI or web)  
- Enter natural language queries related to file content  
- Receive file paths and summaries in response  


## Project Structure
- `indexing.py` — File scanning and embedding creation  
- `retrieval.py` — Vector search with ChromaDB  
- `query_generator.py` — LLM-based answer generation  
- `app.py` — Interactive user interface (CLI or Streamlit)  
