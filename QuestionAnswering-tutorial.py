from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.indexes.vectorstore import VectorstoreIndexCreator
import json
import os

OPENAI_API_KEY='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'

os.system("clear")
print("============")

with open("state_of_the_union.txt") as f:
    state_of_the_union = f.read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(state_of_the_union)

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]).as_retriever()

query = "What did the president say about Justice Breyer"
docs = docsearch.get_relevant_documents(query)

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

# Quickstart
chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
query = "What did the president say about Justice Breyer"
chain.run(input_documents=docs, question=query)

# The stuff chain is a chain that is trained on a variety of tasks, including question answering. It is a good starting point for most use cases. It is also the default chain for the load_qa_chain function.
chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
response = json.dumps(chain({"input_documents": docs, "question": query}, return_only_outputs=True))

print(str(docs))

# Custom Prompt
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer in Italian:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff", prompt=PROMPT)
chain({"input_documents": docs, "question": query}, return_only_outputs=True)


print(response)

# Print Values
# os.system("clear")
# print(embeddings)
# print("docsearch=====================================================")
# print(docsearch)

# print("docs=====================================================")
# print(docs)
# print("docs=====================================================")#
# print(chain.run(input_documents=docs, question=query))