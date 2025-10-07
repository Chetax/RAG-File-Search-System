# The retrieval.py import should be the name of the file containing load_and_query_chroma_db
# Let's assume you've fixed the import path if needed.

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from retrieval import load_and_query_chroma_db # Assuming this is correct

llm=ChatOllama(model='llama3.2:1b')

def query_generator_and_repsonse(query_text: str):
    """
    Finds relevant documents based on the query and uses the LLM to summarize/confirm the relevance.
    """
    try:
        # 1. Retrieval
        chunks = load_and_query_chroma_db(query_text)
    except Exception as e:
        return {
            "llm_response": f"Error during document retrieval: {e}",
            "source_data": [],
            "total_chunks": 0
        }
        
    total_chunks = len(chunks)
    
    if not chunks:
        return {
            "llm_response": f"I couldn't find any documents related to '{query_text}' in the database.",
            "source_data": [],
            "total_chunks": 0
        }

    # 2. Source Processing and Trust Score Calculation (Same as before)
    distances = [chunk.get('raw distance score ', 0) for chunk in chunks]
    min_dist, max_dist = min(distances), max(distances)
    
    file_scores = []
    context = ""

    for chunk in chunks:
        full_path = chunk.get('source', '')
        content = chunk.get('content', '')
        
        # Build context for the LLM
        context += f"Source: {full_path}, Page: {chunk.get('page', 'N/A')}\nSnippet:\n{content}\n---\n"
        
        filename = full_path.split('/')[-1] if full_path else 'unknown_file'
        dist = chunk.get('raw distance score ', 0)
        
        if max_dist - min_dist == 0:
            trust_percent = 100.0
        else:
            trust_percent = (1 - (dist - min_dist) / (max_dist - min_dist)) * 100
        trust_percent = round(trust_percent, 2)
        
        file_scores.append((filename, trust_percent))
    
    # 3. LLM Response Generation (Revised Prompt)
    
    # The new prompt asks the LLM to summarize the findings based on the original user query.
    prompt_template = PromptTemplate.from_template(
        "You are a helpful document retrieval assistant. Your goal is to confirm which files were found and why they are relevant to the user's input.\n\n"
        "USER INPUT: {user_input}\n\n"
        "RELEVANT DOCUMENT CONTEXT (Snippets from the top {total_chunks} matched chunks):\n{context}\n\n"
        "TASK: Based on the snippets provided, summarize your findings. Explicitly mention the **filenames** found and how they relate to the USER INPUT. If the input appears to be a document name or ID, confirm that you've successfully found matching content."
    )
    
    formatted_prompt = prompt_template.format(
        user_input=query_text, 
        total_chunks=total_chunks, 
        context=context
    )
    
    try:
        response_message = llm.invoke([HumanMessage(content=formatted_prompt)])
        llm_response = response_message.content
    except Exception as e:
        llm_response = f"Error during LLM generation: {e}"

    # 4. Return the structured dictionary
    return {
        "llm_response": llm_response,
        "source_data": file_scores,
        "total_chunks": total_chunks
    }