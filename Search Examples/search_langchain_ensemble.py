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

level = 'INFOZ'

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

#Set Search and Key Words
k=10
score_threshold = 0.8
search_query = "I like computers by Macbooks"
key_word = "fruit"

# Get the version of langchain
langchain_version = pkg_resources.get_distribution("langchain").version
chroma_version = pkg_resources.get_distribution("chroma").version
# faiss_version = pkg_resources.get_distribution("faiss").version

# # Print the version
if level == 'INFOX':
    print("langchain_version", langchain_version)
    print("chroma_version", chroma_version)                      

## Set local environment variables
OPENAI_API_KEY=os.getenv("OPEN_API_KEY")

# Create Embeddings
embeddings = OpenAIEmbeddings()

# Create a list of documents metadata
doc_list = [
    Document(page_content = "I like apples", metadata = {"title": "Apple","content_id": 1}),
    Document(page_content =  "I like oranges",  metadata = {"title": "Orange","content_id": 2}),
    Document(page_content = "Apples and oranges are fruits", metadata = {"title": "Fruit","content_id": 3}),
    Document(page_content =  "I like computers by Apple",   metadata = {"title": "Computer","content_id": 4}),
    Document(page_content =  "I love fruit juice",  metadata = {"title": "Juice","content_id": 5}),
]

#Build the BM25Retriever
bm25_retriever = BM25Retriever.from_documents(doc_list)
bm25_retriever.k = k

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
vector_store = FAISS.from_documents(doc_list, embedding)

# Use the faiss_retriever to get documents that match the search query
SIMILARITY_retreiver = vector_store.as_retriever(search_kwargs={"k": k})  ## Used for ensemble retriever
# print("SIMILARITY_retreiver", SIMILARITY_retreiver)
SIMILARITY_results =vector_store.similarity_search_with_score(search_query, k=k)

# Print the results
if level == 'INFO':
    if SIMILARITY_results:
        for doc, score in SIMILARITY_results:
            similarity_score = round(1 -score, 2)
            print(f"Document: {doc}, Similarity Score: {score}")
    else:
        print("No relevant documents found.")

SIMILARITY_relevant_documents = []
for idx, (doc, score) in enumerate(SIMILARITY_results):
    similarity_score = round(1 - score, 2)
    if similarity_score > score_threshold:
        SIMILARITY_relevant_documents.append((idx,doc.page_content,doc.metadata, score))

# Print the results
if level == 'INFO':
    for doc in SIMILARITY_relevant_documents:
        score = doc[3]
        similarity_score = round(1 - score, 2)
        print(f"Document: {doc}, Similarity Score: {similarity_score}")
else:
    print("No relevant documents found.")


# Create ensemble result
ensemble_result = []

# Get documents from SIMILARITY_results where the content_id matches the content_id from BM25_results
for doc_bm25 in BM25_relevant_documents:
    x = doc_bm25[2]['content_id']
    #print("x", x)
    for (doc_similarity,score) in SIMILARITY_results:
        y = doc_similarity.metadata['content_id']
        #print ("y", y)
        if x == y:
            print("Match")
            ensemble_result.append((doc_similarity,1-score))
print("Custom Ensemble Result: ", ensemble_result)    


# Create ensemble retriever
# Does not work as expected, unable to process search query and key_word togther.
ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever,SIMILARITY_retreiver], weights=[0.5,0.5])  
#docs = ensemble_retriever.get_relevant_documents(key_word, search_query)
docs = ensemble_retriever.get_relevant_documents(key_word)
print("Ensemble Retreiver Result: ", docs)