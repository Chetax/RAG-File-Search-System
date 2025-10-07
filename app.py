import streamlit as st
import os
import subprocess
from pathlib import Path
import shlex 
from query_generator import query_generator_and_repsonse # Ensure this import is correct

# --- 1. Initialize Session State ---
if 'search_results' not in st.session_state:
    st.session_state.search_results = None

home_folder = os.path.expanduser("~")

# --- Function to Open the File or Folder ---
def open_file_or_folder_on_mac(target_path):
    """
    Opens a specified file or folder on macOS using the 'open' command.
    """
    # Check if the path exists before proceeding
    if not os.path.exists(target_path):
        st.error(f"Error: Target path not found: {target_path}")
        return

    try:
        # Use shlex.quote to safely handle paths with spaces or special characters
        # This is CRITICAL for paths containing spaces, which often breaks subprocess calls.
        quoted_path = shlex.quote(target_path)
        command = f"open {quoted_path}"
        
        # Use subprocess.run with shell=True for reliable execution of the command string
        subprocess.run(command, shell=True, check=True) 
        
        # Determine what was opened for the toast message
        item_name = os.path.basename(target_path)
        
        st.toast(f"✅ Attempting to open: {item_name}", icon='📄')
        print(f"Successfully executed command: {command}")
        
    except subprocess.CalledProcessError as e:
        # This catches errors if the shell command itself returns a non-zero exit code
        st.error(f"Error executing 'open' command (Check permissions or if a reader is installed): {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred during command execution: {e}")

# --- Streamlit App Setup ---
st.set_page_config(page_title="Document Retrieval System", layout="wide")
st.title("📄 Document Retrieval System")
st.markdown("Enter your query to find the location of the relevant files and **open them locally**.")

user_query = st.text_input(
    "Your Query/Content:",
    placeholder="e.g., steuernr. : 205/5809/1828"
)

# --- 2. Button to Trigger Search and Save Results ---
if st.button("Find Files"):
    if user_query:
        with st.spinner("Searching documents..."):
            try:
                # Call the retrieval function
                results = query_generator_and_repsonse(user_query)
                # 3. Store results in session state
                st.session_state.search_results = results
                st.success("Search complete!")
            except Exception as e:
                st.error(f"Error calling retrieval function: {e}")
                st.session_state.search_results = None
    else:
        st.error("Please enter a query to proceed.")

st.divider()

# --- 4. Display Logic (Always Runs if results exist in session state) ---
results = st.session_state.search_results

if results:
    
    st.markdown(f"**Status:** {results.get('llm_response', 'Results retrieved.')}")

    # --- Display Source Information ---
    st.header(f"📚 Sources Found ({results.get('total_chunks', 0)} Chunks)")
    
    source_data = results.get("source_data", [])
    
    if source_data:
        st.subheader("Relevant Sources and Trust Score")
        
        col1, col2, col3 = st.columns([3, 1, 1.5])
        
        col1.markdown("**Filename**") 
        col2.markdown("**Trust %**")
        col3.markdown("**Action**")
        
        # Iterate through the sources
        for i, (filename, trust, full_path) in enumerate(source_data):
            
            if trust >= 70: color = "green"
            elif trust >= 40: color = "orange"
            else: color = "red"
            
            col1.markdown(f"**{filename}**")
            col2.markdown(f":{color}[**{trust}%**]")

            
            # --- The target path is the full path of the file ---
            target_path = full_path
            
            # 5. Button now calls the function with the file path
            if col3.button("Open File", key=f"open_btn_{i}", help=f"Open {filename} in your local reader"):
                open_file_or_folder_on_mac(target_path)
        
            with col1.expander(f"Full Path for {filename}"):
                st.code(full_path, language=None) 

    else:
        st.warning("No relevant document chunks were found for this query.")
