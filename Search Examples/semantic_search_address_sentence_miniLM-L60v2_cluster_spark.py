from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.ml.linalg import Vectors
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import DBSCAN
import numpy as np

# Create a Spark session
spark = SparkSession.builder.getOrCreate()

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

# Convert the list of addresses to a DataFrame
df = spark.createDataFrame([(t,) for t in addresses], ["address"])

# Define a UDF that converts an address to a vector
@udf("array<float>")
def encode(address):
    return model.encode([address])[0].tolist()

# Add a new column to the DataFrame with the vectors
df = df.withColumn("vector", encode(df["address"]))

# Convert the vectors to a numpy array
vectors = np.array(df.select("vector").rdd.flatMap(lambda x: x).collect())

# Calculate the cosine distance matrix
distance_matrix = cosine_distances(vectors)

# Cluster the addresses using DBSCAN
clustering = DBSCAN(metric='precomputed', eps=0.2, min_samples=2).fit(distance_matrix)

# Add the cluster labels to the DataFrame
df = df.withColumn("cluster", clustering.labels_)

# Show the DataFrame
df.show()