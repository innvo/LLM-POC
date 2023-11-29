from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.indexes.vectorstore import VectorstoreIndexCreator
import json
import pinecone
import os

#3#Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

## Set local environment variables
embeddings = OpenAIEmbeddings()
pinecone.init(api_key="ef9a9434-5233-4b29-a794-355b106be8d7",
              environment="us-west4-gcp-free")
index_name = "llm-demo"

# Create a Pinecone index object
index = pinecone.Index(index_name=index_name)

## Question
query_string = "What did the president say about Justice Breyer" 
## Generate the query embedding
query_embedding = embeddings.embed_query(query_string)

## Perform the query
search_results = index.query(query_embedding, top_k=3, include_metadata=True, include_values=False)

## Print the search results
print("Search results:", search_results)


