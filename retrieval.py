import os
from langchain.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings 
from indexing import create_embedding_and_store_in_croma_db
from dotenv import load_dotenv 
load_dotenv()

def load_and_query_chroma_db(query_text:str):
    persist_dir = os.getenv("PERSIST_DIRECTORY")
    if not os.path.isdir(persist_dir):
        create_embedding_and_store_in_croma_db()

    embeddings = OllamaEmbeddings(
        model=os.getenv("EMBEDDING_MODEL"),
    )

    vector_store = Chroma(
        persist_directory= os.getenv("PERSIST_DIRECTORY"),
        embedding_function=embeddings,
        collection_name=os.getenv("COLLECTION_NAME")
    )
    
    print(f"Successfully loaded vector store from {os.getenv("PERSIST_DIRECTORY")} folder.")
    print(f"Total chunks found in collection: {vector_store._collection.count()}")
    retrieved_docs = vector_store.similarity_search_with_score(query_text, k=3) 

    return retrieved_docs
