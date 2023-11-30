#Postgres database requires pg_trgm extension to be installed


import psycopg2
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

db_user=os.getenv("DBUSER")
db_password=os.getenv("DBPASSWORD")
db_host=os.getenv("DBHOST")

def generate_query(name):
    # Split the name into tokens
    tokens = name.split()

    # Generate the SQL query
    query = "SELECT id, name FROM name_table WHERE "
    #query += " OR ".join([f"SOUNDEX(name) LIKE CONCAT(SOUNDEX('{token}'),' %')" for token in tokens])
    query += " OR ".join([f"name % '{token}'" for token in tokens])

    return query

def execute_query(query):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="llm-demo",
        user=db_user,
        password=db_password,
        host=db_host,
        port="5432"
        )

    # Create a cursor object
    cur = conn.cursor()

    # Execute the query
    cur.execute(query)

    # Fetch all the rows
    rows = cur.fetchall()

    # Close the database connection
    conn.close()

    return rows

def calculate_similarity(name, rows):
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate the embedding for the provided name
    name_embedding = model.encode([name])
    print(f"Embedding for '{name}': {name_embedding}")

    for row in rows:
        # Generate the embedding for the current row
        row_embedding = model.encode([row[0]])

        # Calculate the cosine similarity
        similarity = cosine_similarity(name_embedding, row_embedding)

        # Print the similarity
        print(f"Similarity between '{name}' and '{row[0]}': {similarity[0][0]}")

def calculate_char_similarity(name, rows):
    # Initialize the CountVectorizer
    vectorizer = CountVectorizer(analyzer='char')

    for row in rows:
        # Generate the character-based embeddings
        embeddings = vectorizer.fit_transform([name, row[0]])

        # Calculate the cosine similarity
        similarity = cosine_similarity(embeddings[0:1], embeddings[1:2])

        # Print the similarity
        print(f"Similarity between '{name}' and '{row[0]}': {similarity[0][0]}")

# Example usage:
name = "CHASIN ERIC"
query = generate_query(name)
rows = execute_query(query)
calculate_similarity(name, rows)
calculate_char_similarity(name, rows)

for row in rows:
    print(row)