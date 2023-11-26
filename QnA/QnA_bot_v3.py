
# Python program that reads files from a folder, creates embeddings using OpenAI, stores them in a Chromata vectorstore, 
# and responds to user questions using OpenAI LLM with prompt engineering to ensure correct answers:
import os
import re
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import PGEmbedding
import openai
import psycopg2
from PyPDF2 import PdfReader
from docx import Document
import pdfminer
import spacy


# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

folder_path = "QnA/country_reports/content"
chunk_size=500
overlap = 50
OPENAI_API_KEY='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'

files = os.listdir(folder_path)

## Process pdf document
def process_pdf_document(full_path):
    print("process_pdf_document: " + full_path)
    pdf = PdfReader(open(full_path, "rb"))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    with open(full_path.replace('.pdf', '.txt'), 'w') as txt_file:
        txt_file.write(text)
    # Create chunks
    chunks = chunk_text(text, chunk_size, overlap)
    print("Number of records in chunks A: " + str(len(chunks)))
    embedding_vectors = create_embeddings_gpt3(chunks)
    write_to_pg_vectorstore(embedding_vectors)
    #print("Number of chunks is list: ",chunks[0])

## Process docx document
def process_docx_document(full_path):
    print("process_docx_document: " + full_path)
    doc = Document(full_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    with open(full_path.replace('.docx', '.txt'), 'w') as txt_file:
        txt_file.write(text)
    # Create chunks
    chunks = chunk_text(text, chunk_size, overlap)
    # print the number of chunks
    print("Number of records in chunks A: " + str(len(chunks)))
 
   

## Chunk text
def chunk_text(text, chunk_size, overlap):
    chunks = []
    current_chunk = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i+chunk_size]
        # Cleanse chunk
        chunk = cleanse_text(chunk)
        # print(" starting token: " + str(i) + " " + "chunk_text: " + str(chunk))
        current_chunk.append(chunk)
        # print("current_chunk: " + str(i) + " " + str(chunk))
        # Maintain overlap between chunks
        if i + chunk_size + overlap < len(text):
            current_chunk.append(text[i+chunk_size:i+chunk_size+overlap])
        chunks.append(current_chunk)
    print("Number of records in chunks AB: " + str(len(chunks)))
    return chunks

## Cleanse text
def cleanse_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Convert all characters to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Strip leading and trailing whitespace
    text = text.strip()
    # Replace \n with a space
    text = text.replace('\n', '')
    return text

## Create embeddings
def create_embeddings_gpt3(chunks):
    embeddings = OpenAIEmbeddings() # Load the Langchain OpenAI client
    embedding_vectors = []
    for i, chunk in enumerate(chunks):      
        if chunk[i] != ' ': # Skip empty chunks.  THIS SHOULD BE FIXED in Chunks
            print("chunk number: " + str(i) + " chunk string: " +  chunk[i])
            # Create embeddings
            vectors = embeddings.embed_query(chunk[i])
            # print("query_result: " + str(vectors))
            # Create a tuple of chunk and corresponding embedding vectors
            chunk_and_vectors = (chunk[i], vectors)
            # Append the tuple to the embedding_vectors array
            embedding_vectors.append(chunk_and_vectors)
    return embedding_vectors

def write_to_pg_vectorstore(embedding_vectors):
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=tp-dev.cr7ro0ecjzwg.us-east-1.rds.amazonaws.com port=5432")
    # Open a cursor to perform database operations
    cur = conn.cursor()

    for i, (chunk, vector) in enumerate(embedding_vectors):
        # Execute a query
        cur.execute("INSERT INTO QnA_bot_vectorstore (id, chunk, vector) VALUES (%s, %s, %s)", (i, chunk, vector))
    # Commit changes
    conn.commit()


    # Close cursor and connection
    cur.close()
    conn.close()



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
      