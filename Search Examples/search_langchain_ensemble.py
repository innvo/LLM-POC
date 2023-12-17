#!pip install rank_bm25
# 
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.schema import Document
from langchain.vectorstores import chroma
from langchain.vectorstores import FAISS
import logging
import os
import pkg_resources


# Configure the logging module to output diagnostic information
# logging.basicConfig(level=logging.INFO)
# 
level = 'INFO'

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Get the version of langchain
langchain_version = pkg_resources.get_distribution("langchain").version
chroma_version = pkg_resources.get_distribution("chroma").version
# faiss_version = pkg_resources.get_distribution("faiss").version

# # Print the version
if level == 'INFO':
    print("langchain_version", langchain_version)
    print("chroma_version", chroma_version)                      

## Set local environment variables
OPENAI_API_KEY=os.getenv("OPEN_API_KEY")

embeddings = OpenAIEmbeddings()

# Create a list of documents metadata
doc_list = [
    Document(page_content = "I like apples", metadata = {"title": "Apple","content_id": 1}),
    Document(page_content =  "I like oranges",  metadata = {"title": "Orange","content_id": 2}),
    Document(page_content = "Apples and oranges are fruits", metadata = {"title": "Fruit","content_id": 3}),
    Document(page_content =  "I like computers by Apple",   metadata = {"title": "Computer","content_id": 4}),
    Document(page_content =  "I love fruit juice",  metadata = {"title": "Juice","content_id": 5}),
]

# Extract the text from each document
#doc_texts = [doc["text"] for doc in doc_list]

#Build the BM25Retriever
bm25_retriever = BM25Retriever.from_documents(doc_list)
bm25_retriever.k = 2

#Set Search and Key Words
search_query = "I like computers by Macbooks"
key_word = "computer"

#Retrieve Documents
BM25_results = bm25_retriever.get_relevant_documents(key_word)
if level == 'INFO':
    print("BM25_results", BM25_results)

# Filter out documents that do not include the keyword
BM25_relevant_documents = []
if BM25_results :
    for idx, doc in enumerate(BM25_results):
        if key_word in doc.page_content:
            BM25_relevant_documents.append((idx,doc.page_content,doc.metadata))

if level == 'INFO':
    if BM25_relevant_documents:
     print("bm25_retriever: ')", BM25_relevant_documents)
    else:
        print("No relevant documents found.")

#Create Embeddings
embedding = OpenAIEmbeddings()

#Dense Retreiver
faiss_vector_store = FAISS.from_documents(doc_list, embedding)

# Use the faiss_retriever to get documents that match the search query
FAISS_results =faiss_vector_store.similarity_search_with_score(search_query, k=1)

# Print the results
if level == 'INFO':
    if FAISS_results:
        for doc, score in FAISS_results:
            similarity_score = round(1 -score, 2)
            print(f"Document: {doc}, Similarity Score: {similarity_score}")
    else:
        print("No relevant documents found.")


# Use the relevant documents as input to the ensemble retriever
# BM25_results = relevant_documents

# print ("BM25_results", BM25_results)