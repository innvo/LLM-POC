
# Python program that reads files from a folder, creates embeddings using OpenAI, stores them in a Chromata vectorstore, 
# and responds to user questions using OpenAI LLM with prompt engineering to ensure correct answers:
import os
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from PyPDF2 import PdfReader
from docx import Document
import spacy


# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

folder_path = "QnA/country_reports/content"
chunk_size = 500
overlap = 50

files = os.listdir(folder_path)

def process_pdf_document(full_path):
 def process_pdf_document(full_path):
    print("process_pdf_document: " + full_path)
    pdf = PdfReader(open(full_path, "rb"))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    with open(full_path.replace('.pdf', '.txt'), 'w') as txt_file:
        txt_file.write(text)

def process_docx_document(full_path):
    print("process_docx_document: " + full_path)
    doc = Document(full_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    with open(full_path.replace('.docx', '.txt'), 'w') as txt_file:
        txt_file.write(text)
    # create chunks
    chunks = chunk_text(text, chunk_size, overlap)

## Chunk text
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    current_chunk = []

    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i+chunk_size]
        print(" starting token: " + str(i) + " " + "chunk_text: " + str(chunk))
        current_chunk.append(chunk)
        # Print current chunk
        # print("current_chunk: " + str(current_chunk))
        # Maintain overlap between chunks
        if i + chunk_size + overlap < len(text):
            current_chunk.append(text[i+chunk_size:i+chunk_size+overlap])
    chunks.append(current_chunk)
    return chunks


for file in files:
    if file.endswith('.pdf'):
        full_path = os.path.join(folder_path, file)
        #print(" In pdf: " + full_path)
        process_pdf_document(full_path)
        # document = PyPDFLoader(os.path.join(folder_path, file))
        # pages = loader.load_and_split()
        # do something with pages
        # print(document)
    if file.endswith('.docx'):
        full_path = os.path.join(folder_path, file)
        # print(" In docx: " + full_path)
        process_docx_document(full_path)
      