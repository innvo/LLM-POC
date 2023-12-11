from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Create a SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the addresses
address1 = '123 Apple St UNIT 1 New York NY'
address2 = '123 Maple Street New York New York 22012'

# Convert the addresses to vectors
vector1 = model.encode([address1])[0]
vector2 = model.encode([address2])[0]

print(vector1)

# Calculate the cosine similarity between the vectors
similarity = cosine_similarity([vector1], [vector2])[0][0]

print(f"The cosine similarity between '{address1}' and '{address2}' is {similarity}")