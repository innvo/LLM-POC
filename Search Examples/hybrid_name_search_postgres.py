#Postgres database requires pg_trgm extension to be installed


import psycopg2
import os
import warnings
import pandas as pd 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

db_user=os.getenv("DBUSER")
db_password=os.getenv("DBPASSWORD")
db_host=os.getenv("DBHOST")
warnings.filterwarnings("ignore")

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

def generate_query(name):
    # Split the name into tokens
    tokens = name.split()

    # Generate the SQL query
    query = "SELECT id, name FROM name_table WHERE "
    #query += " OR ".join([f"SOUNDEX(name) LIKE CONCAT(SOUNDEX('{token}'),' %')" for token in tokens])
    query += " OR ".join([f"name % '{token}'" for token in tokens]
    )

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

def calculate_similarity(name, rows, threshold=0.8):
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate the embedding for the provided name
    name_embedding = model.encode([name])

    # List to store rows with similarity greater than threshold
    similar_rows = []

    for row in rows:
        # Generate the embedding for the current row
        row_embedding = model.encode([row[1]])

        # Calculate the cosine similarity
        similarity = cosine_similarity(name_embedding, row_embedding)

        # If the similarity is greater than the threshold, add the row to the list
        if similarity[0][0] > threshold:
            print(f"Similarity (sentence) between '{name}' and '{row[1]}' (id: {row[0]}): {similarity[0][0]}")
            similar_rows.append(row)

    return similar_rows

def calculate_char_similarity(name, rows, threshold=0.80):
    # Initialize the CountVectorizer
    vectorizer = CountVectorizer(analyzer='char')

    # List to store rows with similarity greater than threshold
    similar_rows_char = []

    for row in rows:
        # Generate the character-based embeddings
        embeddings = vectorizer.fit_transform([name, row[1]])

        # Calculate the cosine similarity
        similarity = cosine_similarity(embeddings[0:1], embeddings[1:2])

        # If the similarity is greater than the threshold, add the row to the list
        if similarity[0][0] > threshold:
            # Print the similarity
            print(f"Similarity (char) between '{name}' and '{row[1]}' (id: {row[0]}): {similarity[0][0]}")
            similar_rows_char.append(row)

    return similar_rows_char

def execute_sql(ids):
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

    # Generate the SQL query
    query = "SELECT * FROM name_table WHERE id IN %s "
    cur.execute(query, (tuple(ids),))

    # Fetch all the rows
    rows = cur.fetchall()

    # Close the database connection
    conn.close()

    # Create a DataFrame from the rows
    node_df = pd.DataFrame(rows, columns=["id", "name"]) 

    return node_df

# Example usage:
name = "ERIC CHASIN"
query = generate_query(name)
rows = execute_query(query)
calculate_similarity(name, rows)
calculate_char_similarity(name, rows)
similar_rows_char = calculate_char_similarity(name, rows)

# Extract the ids from similar_rows_char
ids = [row[0] for row in similar_rows_char]

# Execute the SQL query
node_df=execute_sql(ids)

# Display the DataFrame
print(node_df)