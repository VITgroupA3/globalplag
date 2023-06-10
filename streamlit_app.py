import requests
import streamlit as st
from PyPDF2 import PdfReader

# Replace with your Plagly API key
API_KEY = 'WsvCMDOVNhUSGrB5X1E3dFzxZ3Y61Atd'


def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except PdfReader.PdfReadError as e:
        st.error("Error: Invalid PDF file.")
        st.stop()


def check_plagiarism(text):
    url = 'https://api.plagly.com'
    headers = {
        'Content-Type': 'text/plain',
        'apikey': API_KEY
    }
    response = requests.post(url, headers=headers, data=text.encode('utf-8'))
    plagiarism_report = response.json()
    return plagiarism_report


def main():
    st.title("Plagiarism Checker")

    file = st.file_uploader("Upload a PDF file")
    if file is not None:
        text = extract_text_from_pdf(file)
        plagiarism_report = check_plagiarism(text)

        st.header("Plagiarism Report")
        if 'results' in plagiarism_report:
            for result in plagiarism_report['results']:
                st.write(f"Similarity: {result['score']}%")
                st.write(f"Original Text: {result['source']['snippet']}")
                st.write(f"Plagiarized Text: {result['target']['snippet']}")
                st.write("---")
        else:
            st.write("No plagiarism results found.")


if __name__ == '__main__':
    main()
