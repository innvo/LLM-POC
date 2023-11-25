# https://python.langchain.com/en/latest/modules/indexes/vectorstores/examples/pinecone.html
# export OPENAI_API_KEY=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

import getpass
from langchain import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
import openai
import os
import pinecone

pinecone.init(api_key="ef9a9434-5233-4b29-a794-355b106be8d7",
              environment="us-west4-gcp-free")

# Create Pinecone Index - Run Once
# pinecone.create_index("example-index", dimension=1024)

loader = TextLoader('state_of_the_union.txt')
docs = loader.load()

# Split into chunks of 1000 characters
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs_split = text_splitter.split_documents(docs)
docs_split

embeddings = OpenAIEmbeddings()

doc_db = Pinecone.from_documents(
    docs_split, 
    embeddings, 
    index_name='langchain-demo'
)


query = "What did the president say about Ketanji Brown Jackson"
search_docs = doc_db.similarity_search(query)

os.system("clear")
print("docs ============")
print(docs)
print("docs_split ============")
print(docs_split)
print("search_docs ============")
print(search_docs)





# print(active_indexes)
# print(index_description)
# index_stats_response = index.describe_index_stats()
