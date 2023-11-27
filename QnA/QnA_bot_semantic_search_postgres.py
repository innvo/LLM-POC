from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.indexes.vectorstore import VectorstoreIndexCreator
import json
import os

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

embeddings = OpenAIEmbeddings()
## No Match
#query_string = "What did the president say about Justice Breyer" 
## Exact Match
# query_string ="to exploitative working conditions such as working excessive hours or having their wages withheld mainly in domestic labor page 26"
query_string ="what types of abuses do you see"


query_embedding = embeddings.embed_query(query_string)

print(len(query_embedding)) # Should be 1536, the dimensionality of OpenAI embeddings
print(query_embedding[:1536]) # Should be a list of floats

