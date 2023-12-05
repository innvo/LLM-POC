import psycopg2
import pandas as pd
import jellyfish
import os

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

db_user=os.getenv("DBUSER")
db_password=os.getenv("DBPASSWORD")
db_host=os.getenv("DBHOST")


def create_dataframe():
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

    # Execute a SQL query to fetch all rows from the node table
    cur.execute("SELECT id, name FROM name_table")

    # Fetch all the rows
    rows = cur.fetchall()

    # Close the database connection
    conn.close()

    print(rows)

    # Initialize lists to store the DataFrame data
    node_ids = []
    node_names = []
    name_tokens_list = []
    soundex_tokens_list = []

    for row in rows:
        # Split the node_name into tokens
        name_tokens = row[1].split()

        # Calculate the Soundex value for each token
        soundex_tokens = [jellyfish.soundex(token) for token in name_tokens]

        # Add the data to the lists
        node_ids.append(row[0])
        node_names.append(row[1])
        name_tokens_list.append(name_tokens)
        soundex_tokens_list.append(soundex_tokens)

    # Create a DataFrame
    df = pd.DataFrame({
        "node_id": node_ids,
        "node_name": node_names,
        "name_tokens": name_tokens_list,
        "soundex_tokens": soundex_tokens_list
    })

    return df

# Create the DataFrame
df = create_dataframe()

print(df.head())