import openai
import os
from dotenv import load_dotenv
import streamlit as st
import PyPDF2
from PyPDF2 import PdfReader
import docx

import json
import requests

load_dotenv(override=True)
openai.api_key=os.getenv("OPEN_API_KEY")
def read_pdf(file_path):
    pdf = PdfReader(file_path)
    text = ''
    for page in pdf.pages:
        text += page.extract_text()
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
    return text

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    response_message = response.choices[0].message.content
    return response_message

# Streamlit UI
st.title("Document-based Question Answering System")
file_path = st.file_uploader("Upload PDF/Docx/txt",type=["pdf","docx","txt"])

question = st.text_input('Enter your question:')


if st.button('Get Answer'):
    if file_path.type=='application/pdf':
            document_text = read_pdf(file_path)
    elif file_path.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            document_text = read_docx(file_path)
    elif file_path.type=="text/plain":
           document_text = file_path.read().decode('utf-8')
    else:
            st.error('Unsupported file format')
            st.stop()

    prompt = f"""Your task is to answer the question asked based on the document provided by the user and also subtopics if the user asks.\n\nDocument:```{document_text,question}```"""
    answer = get_completion(prompt)
    st.success(f"Answer: {answer}")
        
  
