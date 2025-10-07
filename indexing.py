import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document 
from langchain.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from dotenv import load_dotenv 
load_dotenv()

TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1000,       
    chunk_overlap=200,      
    separators=["\n\n", "\n", " ", ""] 
)

def load_and_chunk_files():
    dir = r"/Users/consultadd/Projects/RAG_Ollama/Folder-From-Which-We-Will-Read-All-Files"
    file_paths = []
    
    try:
        with os.scandir(dir) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.lower().endswith('.pdf'):
                    file_paths.append(entry.path)
    except FileNotFoundError:
        print(f"Error: Directory not found at {dir}")
        return []

    all_chunks: list[Document] = []

    for path in file_paths:
        try:
            loader = PyPDFLoader(path) 
            page_docs: list[Document] = loader.load()
            
            if not page_docs:
                print(f"File loaded successfully but contained no pages: {path}")
                continue
            
            chunks = TEXT_SPLITTER.split_documents(page_docs)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"Could not load document from {path}. Error: {e}")

    return all_chunks 


def create_embedding_and_store_in_croma_db():
    
    chunked_docs = load_and_chunk_files() 
    
    if not chunked_docs:
        print("No chunks were created. Aborting vector store creation.")
        return

    embeddings = OllamaEmbeddings(
        model=os.getenv("EMBEDDING_MODEL"),
    )
    
    vector_store = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        persist_directory=os.getenv("PERSIST_DIRECTORY"),
        collection_name=os.getenv("COLLECTION_NAME")
    )
    
    vector_store.persist() 
    print(f"\nSuccessfully stored {len(chunked_docs)} chunks in Chroma DB.")

