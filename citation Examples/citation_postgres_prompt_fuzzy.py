from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import create_citation_fuzzy_match_chain
from langchain.chat_models import ChatOpenAI
#from langchain.chains.question_answering import load_qa_chain
#from langchain_community.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.llms import OpenAI
import langchain
import os
import psycopg2
import warnings
warnings.filterwarnings('ignore')


# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

embeddings = OpenAIEmbeddings()
## Set local environment variables
folder_path = "QnA/country_reports/content"
OPENAI_API_KEY=os.getenv("OPEN_API_KEY")
db_user=os.getenv("DBUSER")
db_password=os.getenv("DBPASSWORD")
db_host=os.getenv("DBHOST")

## Langchain setup
#model = langchain.OpenAI(temperature=0, model_name="gpt-3.5-turbo-0613")  ## This does not work
model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613")
embeddings = OpenAIEmbeddings()

def highlight(text, span):
    return (
        "..."
        + text[span[0] - 20 : span[0]]
        + "*"
        + "\033[91m"
        + text[span[0] : span[1]]
        + "\033[0m"
        + "*"
        + text[span[1] : span[1] + 20]
        + "..."
    )

## search emebedding
def search_embedding(query_string):
    print("in search_embedding")
    query_embedding = embeddings.embed_query(query_string)
    return query_embedding

## similarity_search
def get_documents(question):
    print("in similarity_search")
    docs= []
    query_embedding = search_embedding(question)
    # print("query_embedding: " + str(query_embedding))
    conn = psycopg2.connect(
        dbname="llm-demo",
        user=db_user,
        password=db_password,
        host=db_host,
        port="5432"
        )
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute aquery
    cur.execute(f""" select id, embedding_content, 
                 1 - (embedding_vector <=> '{query_embedding}') as cosine_similarity 
                 from public.contentembedding 
                 order by 3 desc
                 limit 20""") 
    # Fetch all results
    results = cur.fetchall()

    # Close cursor and connection
    cur.close()
    conn.close()

    # Create docs list for langchain Qa Chain
    for i, result in enumerate(results):   
        doc = Document(
            #citation_id=result[0],
            page_content=result[1],
            metadata={"content_id": result[0]}
        )
        chain = create_citation_fuzzy_match_chain(model)
        context = doc.page_content
        metadata={"content_id": result[0]}
        #print("question: " + question)
        #print("context: " + context) 
        if question is not None and context is not None:
            print("XXXX")

            result = chain.run(question=question, context=context, metadata=metadata)
            #print(result)

    for fact in result.answer:
        #print("Content:", result)
        print("Metadata:", metadata)
        print("Statement:", fact.fact)
        for span in fact.get_spans(context):
            print("Citation:", highlight(context, span))
        print()
    
        # print("doc.content_id " + str(i) + ' ' + str(doc.metadata['content_id']))
        # docs.append(doc)    
    # get_response_from_llm(docs)
  
## Get response from langchain Qa Chain   
# def get_response_from_llm(docs):
#     # Load QA Chain
#     chain = create_citation_fuzzy_match_chain(model)
#     response = chain.run(
#         question=question, 
#         context=docs[0].page_content
#     ) 
#     #print(response, docs[0].metadata['content_id'] )
#     print(response)





## Generate the query embedding 
def answer_question(question):
    get_documents(question)


###############################
#question =  "What did the president say about Justice Breyer" 
#question =  "What did the president say about immigration. Provide 5 as bullets.  be concise"   
#question =  "What did the president Biden say about southern border in in speech February 2023. Provide 3 as bullets. If the user does no provide a timeframe in his question,  ask the user to provide a timeframe to find content"
#question =  "What did the president biden say about southern border provide as 5 bullets"
question = "What are the top 10 topics discussed by president. For every sentence in the response cite the content_id"
#question = "What is the president' birthday"

answer_question(question)


