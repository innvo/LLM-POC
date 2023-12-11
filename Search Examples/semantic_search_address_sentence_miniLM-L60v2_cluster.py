from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import DBSCAN

# Create a SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the addresses
addresses = [
    '123 Apple St UNIT 1 New York NY',
    '123 Maple Street New York New York 22012',
    '123 Apple Street Unit 1 NY, NY',
    '123 Maple St New York NY',
    # Add more addresses here
]

# Convert the addresses to vectors
vectors = model.encode(addresses)

# Calculate the cosine distance matrix
distance_matrix = cosine_distances(vectors)

# Cluster the addresses using DBSCAN
clustering = DBSCAN(metric='precomputed', eps=0.2, min_samples=2).fit(distance_matrix)

# Print the cluster labels for each address
for address, cluster_label in zip(addresses, clustering.labels_):
    print(f"The address '{address}' is in cluster {cluster_label}")