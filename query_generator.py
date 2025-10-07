# Save this in your query_generator.py (or wherever the function is defined)

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from retrieval import load_and_query_chroma_db 

# Note: LLM is no longer used, but keeping the declaration for module completeness
llm=ChatOllama(model='llama3.2:1b')

def query_generator_and_repsonse(query_text: str):
    """
    Finds relevant documents based on the query and returns source links and trust scores.
    (LLM summarization logic has been removed as per user request).
    """
    try:
        # 1. Retrieval
        chunks = load_and_query_chroma_db(query_text)
    except Exception as e:
        # Return a structure that the frontend can handle, even on error
        return {
            "llm_response": f"Error during document retrieval: {e}",
            "source_data": [],
            "total_chunks": 0
        }
        
    total_chunks = len(chunks)
    
    if not chunks:
        # Provide a simple, direct message when no files are found
        return {
            "llm_response": f"I couldn't find any documents related to '{query_text}' in the database.",
            "source_data": [],
            "total_chunks": 0
        }

    # 2. Source Processing and Trust Score Calculation
    distances = [chunk.get('raw distance score ', 0) for chunk in chunks]
    min_dist, max_dist = min(distances), max(distances)
    
    # *** CRITICAL CHANGE: file_scores now stores (filename, trust, full_path) ***
    file_scores = []
    
    for chunk in chunks:
        full_path = chunk.get('source', '')
        # content is no longer needed for LLM context, but can be kept for debugging
        
        filename = full_path.split('/')[-1] if full_path else 'unknown_file'
        dist = chunk.get('raw distance score ', 0)
        
        if max_dist - min_dist == 0:
            trust_percent = 100.0
        else:
            trust_percent = (1 - (dist - min_dist) / (max_dist - min_dist)) * 100
        trust_percent = round(trust_percent, 2)
        
        # Store the full path along with the filename and trust score
        file_scores.append((filename, trust_percent, full_path))
    
    # 3. CRITICAL: Return the structured dictionary without an LLM call
    # The 'llm_response' key is still returned but contains a simple confirmation.
    return {
        "llm_response": f"Found {total_chunks} relevant document snippets for your query.",
        "source_data": file_scores,
        "total_chunks": total_chunks
    }