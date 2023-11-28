from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone
import langchain
import json
import pinecone
import openai
import os

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

embeddings = OpenAIEmbeddings()
pinecone.init(api_key="ef9a9434-5233-4b29-a794-355b106be8d7",
              environment="us-west4-gcp-free")
# Create a Pinecone index object
index_name = "llm-demo"
index = pinecone.Index(index_name=index_name)

# Langchain setup
model = langchain.OpenAI(temperature=0, model_name="gpt-3.5-turbo")
# qa_prompt = "Human: how many jobs were created?\nAssistant:" ##not using context


# Generate the query embedding
def answer_question(question):
 
    question_emb = embeddings.embed_query(question)

    # Perform the query
    res = index.query([question_emb], top_k=1, include_metadata=True, include_values=False)
    print(res)

    #print(res)
    context = res['matches'][0]['metadata']['embedding_content']
    prompt = f"Human: {question}\nAssistant: Based on the following context: {context}\n"

    # response = model.generate(prompt)
    print(prompt)

     # Get response for each prompt
    responses = model.generate(
        [prompt]
    )

    # Return response list
    return responses

question =  "What did the president say about Justice Breyer" 
answer = answer_question(question)
print(answer)
