import pandas as pd
from sentence_transformers import SentenceTransformer  
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import DBSCAN

# Create model and encode addresses
model = SentenceTransformer('all-MiniLM-L6-v2')
addresses = [
    '123 Apple St UNIT 1 New York NY',
    '123 Maple Street New York New York 22012',
    '123 Apple Street Unit 1 NY, NY',    
    '123 Maple St New York NY',
    '452 Main St New York NY',  
]
vectors = model.encode(addresses)

# Calculate distances and similarities  
distance_matrix = cosine_distances(vectors)
similarity_matrix = 1 - distance_matrix

# Cluster addresses 
clustering = DBSCAN(metric='precomputed', eps=0.2, min_samples=2).fit(distance_matrix)
cluster_labels = clustering.labels_

# Create dataframes  
cluster_df = pd.DataFrame({'Address': addresses, 'Cluster': cluster_labels})
similarity_df = pd.DataFrame(similarity_matrix, columns=addresses, index=addresses)

# Print outputs 
print(cluster_df)
print() 
print(similarity_df.round(3))


# Reset the index of the similarity DataFrame
similarity_df_reset = similarity_df.reset_index()

# Reshape the DataFrame
similarity_df_melt = similarity_df_reset.melt(id_vars='index', var_name='address2', value_name='similarity_score')

# Rename the columns
similarity_df_melt.columns = ['address1', 'address2', 'similarity_score']

# Print the DataFrame
print(similarity_df_melt)
