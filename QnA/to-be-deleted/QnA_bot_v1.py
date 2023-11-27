import os
import PyPDF2
import docx
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import json

def read_files_from_folder(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_file = open(os.path.join(folder_path, filename), 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                print(page_num)
                # page = pdf_reader.pages(page_num)
                # texts.append(page.extractText())
            pdf_file.close()
        elif filename.endswith('.docx'):
            doc = docx.Document(os.path.join(folder_path, filename))
            for para in doc.paragraphs:
                texts.append(para.text)
    return texts


# def get_number_of_pages(file_path):
#     with open(file_path, "rb") as file:
#         reader = PdfFileReader(file)
#         num_pages = len(reader.pages)  # Use len(reader.pages) instead of reader.numPages
#     return num_pages


# Set local environment variables
filefolder = "QnA/country_reports/content"

# Call the function and store the result
texts = read_files_from_folder(filefolder)

# Display the filenames read in the folder
# for filename in os.listdir(filefolder):
#     if filename.endswith('.pdf') or filename.endswith('.docx'):
#         print(filename)