# LLM-POC
This project provides live demonstrations Question and Answer using documents managed by a vectorstore.

## Prerequistes
1. Postgres 14 or higher with vector extension installed
2. OPENAPI api account.  All examples are based on openai embeddings and llms.  Future examples will include opensource llms include Meta LLAMA2
3. Pinecone api account
4. Python 3.0 environment
5. pip to install required libraries

## Postgres vectorstore
1. Create a "llm-demo" database in postgres or change the code to used the default postgres database
2. Create the follwing table to store the embeddings
```
CREATE SEQUENCE contentembedding_id_seq;

CREATE EXTENSION vector

CREATE TABLE public.contentembedding (
    id BIGINT,
    embedding_metadata VARCHAR(1020),
    embedding_content TEXT,
    embedding_vector vector(1536)
);

ALTER TABLE public.contentembedding 
ALTER COLUMN id SET DEFAULT nextval('contentembedding_id_seq');
```

## Pinecone vectorstore
1. Create index "llm-demo"

## QNA Examples
1. create_embeddings_pinecone.py -  creates embeddings for any file in QNA_Examples\content folder.  You can move files from the archive_content folder for testing. embeddings are store in pinecone vector store
2. create_embeddings_postgrese.py -  creates embeddings for any file in QNA_Examples\content folder.  You can move files from the archive_content folder for testing. embeddings are store in postgres vector store
3. QAOverDoc_pinecone.py - Retrieval Augmented Generation using pinecode vectore store and openai gpt-4 api. Based on Langchain QA Chain for a single question/answer
4. QAOverDoc_postgres.py - Retrieval Augmented Generation using postgres vectore store and openai gpt-4 api. Based on Langchain QA Chain for a single question/answer
5. QAOverDocs-tutorial.py - Retrieval Augmented Generation used in memory vector store and openai gpt-4 api.
6. semantic_search_pinecone.py -  used cosine-similarity score to get content  from pinecone vector store
7. semantic_search_postgres.py -  used cosine-similarity score to get content  from postgres vector store
8. state_of_the_union.txt - this used by QAOverDocs-tutorial

# Open Issues
### Release 0.1
1. pinecone api uses upsert.  The current code does not set a unique id.  Please test with single file.  Pinecone does not support truncating indexes.  If the index gets messued you will need to delete and recreate.  This will be address in future release.
2. QAOverDoc_postgres.py - is not functional.  It is partially code.
3. create_embeddings_postgre.py - will truncate the contentembeddings table everytime it runs. I have been testing with 5 files in the archive_content folder



