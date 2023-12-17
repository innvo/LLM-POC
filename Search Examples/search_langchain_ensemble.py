#!pip install rank_bm25
# 
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.schema import Document
from langchain.vectorstores import chroma
from langchain.vectorstores import faiss
import os

import pkg_resources



# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Get the version of langchain
langchain_version = pkg_resources.get_distribution("langchain").version
chroma_version = pkg_resources.get_distribution("chroma").version
# faiss_version = pkg_resources.get_distribution("faiss").version

# # Print the version
print("langchain_version", langchain_version)
print("chroma_version", chroma_version)
# print("faiss_version", faiss_version)

## Set local environment variables
OPENAI_API_KEY=os.getenv("OPEN_API_KEY")

embeddings = OpenAIEmbeddings()

doc_list = [
    "I like apples",
    "I like oranges",
    "Apples and oranges are fruits",
    "I like computers by Apple",
    "I love fuit juice"
]

#Build the BM25Retriever
bm25_retriever = BM25Retriever.from_texts(doc_list)
bm25_retriever.k = 10

#Set Key Words
key_word = "computers"

#Retrieve Documents
retrieved_documents = bm25_retriever.get_relevant_documents(key_word)

# Filter out documents that do not include the keyword
relevant_documents = []
if retrieved_documents:
    for doc in retrieved_documents:
        if key_word in doc.page_content:
            relevant_documents.append(doc.page_content)
        print(doc.page_content)

if relevant_documents:
    print("bm25_retriever.get_relevant_documents('Document(s): ')", relevant_documents)
else:
    print("No relevant documents found.")
