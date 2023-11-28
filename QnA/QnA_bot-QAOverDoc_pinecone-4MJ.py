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

    # Perform the query (Erics Retreiver)
    res = index.query([question_emb], top_k=3, include_metadata=True, include_values=False)
    list
    similiar_docs = get_similiar_docs(question)
    #print(res)

    return res

def get_similiar_docs(query, k=2, score=False): 
    if score:
        similar_docs = index.similarity_search_with_score(query, k=3) 
    else:
        similar_docs = index.similarity_search(query, k=3)
    return similar_docs


#Load QA Chain
chain=load_qa_chain(model, chain_type="stuff")

def get_answer(query):  
    similar_docs = get_similiar_docs(query)  
    print("XXX")
    answer = chain.run(input_documents=similar_docs, question=query)
    #return answer 

query =  "What did the president say about Justice Breyer" 
answer = get_answer(query)
print(answer)
