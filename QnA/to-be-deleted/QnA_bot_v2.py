
# Python program that reads files from a folder, creates embeddings using OpenAI, stores them in a Chromata vectorstore, 
# and responds to user questions using OpenAI LLM with prompt engineering to ensure correct answers:

import os
import pdfplumber
import docx
import openai
import chromadb
# from prompt_engineering import PromptEngineering ERROR: ModuleNotFoundError: No module named 'prompt_engineering'

# Define folder path
folder_path = "QnA/country_reports/content"

# Process files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".pdf"):
        with pdfplumber.open(os.path.join(folder_path, file_name)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
          

    elif file_name.endswith(".docx"):

        with docx.Document(os.path.join(folder_path, file_name)) as doc:
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text

