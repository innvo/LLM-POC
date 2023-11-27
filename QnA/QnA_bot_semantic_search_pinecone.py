from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.indexes.vectorstore import VectorstoreIndexCreator
import json
import pinecone
import os

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

embeddings = OpenAIEmbeddings()
pinecone.init(api_key="ef9a9434-5233-4b29-a794-355b106be8d7",
              environment="us-west4-gcp-free")
index_name = "llm-demo"

# Create a Pinecone index object
index = pinecone.Index(index_name=index_name)

## No Match
#query_string = "What did the president say about Justice Breyer" 
## Exact Match
# query_string ="abductions and physical abuse by nonstate armed groups serious restrictions on freedom of expression including violence threats of violence or unjustified detentions of journalists and censorship substantial interference with the right of peaceful assembly and freedom of association serious restrictions on freedom of movement inability of citizens to change their government peacefully through free and fair elections serious and unreasonable restrictions on political participation serious"
# Partial Match
# query_string ="what is the ruling political party in Cameroon"
query_string ="what types of abuses do you see"
# Generate the query embedding
query_embedding = embeddings.embed_query(query_string)
# print(len(query_embedding)) # Should be 1536, the dimensionality of OpenAI embeddings
#print(query_embedding)


# Perform the query
search_results = index.query(query_embedding, top_k=3, include_metadata=True, include_values=False)

# Print the search results
print("Search results:", search_results)
# for result in search_results:
#     print(result.id, result.score, result.value)




# # Query the index
# results = index.query(
#     vector=[query_embedding],
#     top_k= 1,
#     include_values=True
#     )

# # Print the results
# for result in results.results:
#     print(f"ID: {result.id}, Score: {result.score}")

# Deinitialize Pinecone
# pinecone.deinit()

