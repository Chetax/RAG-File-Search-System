import streamlit as st
# Make sure 'query_generator' is the correct file name containing the function
from query_generator import query_generator_and_repsonse 

# Set up the page
st.set_page_config(page_title="RAG Chatbot Frontend", layout="wide")

# --- Header ---
st.title("📄 Document Retrieval and RAG Chatbot")
st.markdown("Enter your query (e.g., a **Steuernr.** or question) below, and the application will fetch relevant information and provide a response.")

# --- Input ---
user_query = st.text_input(
    "Your Query/Question:",
    placeholder="e.g., steuernr. : 205/5809/1828 or 'What is the due date on invoice_2023.pdf?'"
)

# --- Button and Logic ---
if st.button("Get Response"):
    if user_query:
        # Show a spinner while processing
        with st.spinner("Searching documents and generating response..."):
            # Call the backend function
            results = query_generator_and_repsonse(user_query)
            
        st.success("Processing complete!")

        # --- Display AI Response ---
        st.header("🤖 AI Generated Response")
        # Ensure 'results' is a dictionary before accessing keys
        if isinstance(results, dict) and "llm_response" in results:
            st.info(results["llm_response"])
        else:
            st.error("Error: Could not retrieve a valid response from the backend function.")
            st.write(f"Raw Function Output: {results}") # Helpful for debugging

        st.divider()

        # --- Display Source Information ---
        st.header(f"📚 Sources Found ({results.get('total_chunks', 0)} Chunks)")
        
        # Safely get source data
        source_data = results.get("source_data", [])
        
        if source_data:
            st.subheader("Relevant Sources and Trust Score")
            
            # Use columns for a clean presentation
            col1, col2 = st.columns([3, 1])
            
            col1.markdown("**Filename**")
            col2.markdown("**Trust % (Higher is Better)**")
            
            # Iterate through the sources
            for filename, trust in source_data:
                # Calculate color based on trust score
                if trust >= 70:
                    color = "green"
                elif trust >= 40:
                    color = "orange"
                else:
                    color = "red"
                
                col1.markdown(f"**{filename}**")
                col2.markdown(f":{color}[**{trust}%**]")

        else:
            st.warning("No relevant document chunks were found for this query.")
            
    else:
        st.error("Please enter a query to proceed.")