import streamlit as st
from query_data import query_rag
import pdfplumber
import os
import subprocess
from populate_database import clear_database
DATA_PATH = "data"
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def add_pdf_to_chroma():
    result = subprocess.run(
        ['python', 'populate_database.py'], 
        capture_output=True,  
        text=True
    )
    print('running populate_database.py') 
    if result.returncode == 0:
        st.success(f"PDF added to Chroma DB successfully! Output: {result.stdout}")
    else:
        st.error(f"Failed to add PDF to Chroma DB. Error: {result.stderr}")


def home_page():
    st.title("Upload PDF and Add to Chroma Vector DB")
    clear_files(DATA_PATH)
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if pdf_file is not None:
        pdf_file_path = os.path.join(DATA_PATH, pdf_file.name)
        
        with open(pdf_file_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        
        st.success(f"PDF saved at {pdf_file_path}")
        
        st.write("Extracting text from the PDF...")
        pdf_text = extract_text_from_pdf(pdf_file_path)
        
        if st.button("Add PDF to Chroma DB"):
            add_pdf_to_chroma()
            print('Chroma DB Update Complete')
        

def query_page():
    st.title("Queries for PDF Wizard")

    query_text = st.text_input("Enter your query:")
    
    if query_text:
        st.write("Processing your query...")
        answer = query_rag(query_text)
        st.write(answer)

def clear_files(directory):
    if os.path.exists(directory):
        # Loop through all files and remove them
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error clearing file {file_path}: {e}")
    else:
        os.makedirs(directory)


def main():
    page = st.sidebar.radio("Choose a page", ["Home", "Query"])

    if page == "Home":
        home_page()
    elif page == "Query":
        query_page()

if __name__ == "__main__":
    main()
