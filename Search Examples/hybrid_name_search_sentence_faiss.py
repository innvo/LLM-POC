import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pandas as pd

# Create sample data
person_df = pd.DataFrame({
    "node_id": [1, 2, 3, 4], 
    "name": ["John Smith", "Mary Johnson", "Bob Williams", "Sarah Davis"]
})

model = SentenceTransformer('all-MiniLM-L6-v2')
person_df["embedding"] = person_df["name"].apply(lambda x: model.encode(x))

# Store in FAISS index
index = faiss.IndexFlatIP(384)  # Change dimension to 384
embeddings = np.stack(person_df['embedding'].values)
index.add(embeddings) 

# Query  
query_name = "John Salome"
query_words = query_name.split()

# Initialize lists to store overall indices and distances
overall_indices = []
overall_distances = []

for word in query_words:
    query_embedding = model.encode(word)
    distances, indices = index.search(np.array([query_embedding]), k=2)
    overall_indices.extend(indices[0].tolist())
    overall_distances.extend(distances[0].tolist())

# Remove duplicates and sort by distance
unique_indices, idx = np.unique(overall_indices, return_index=True)
unique_distances = np.array(overall_distances)[idx]

# Sort by distance
sorted_idx = np.argsort(unique_distances)
sorted_indices = unique_indices[sorted_idx]
sorted_distances = unique_distances[sorted_idx]

# Print all results, their scores, and node_id
for i in range(len(sorted_indices)):
    print(f"Node ID: {person_df.iloc[sorted_indices[i]]['node_id']}, Name: {person_df.iloc[sorted_indices[i]]['name']}, Score: {sorted_distances[i]}")