import requests
import os
import json
from sklearn.metrics.pairwise import cosine_similarity

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Define a function to get the word vector from flask server
# Define a function to get the word vector from flask server
def get_word_vector(word):
    response = requests.post('http://127.0.0.1:5000/use_model', json={'word': word})
    return json.loads(response.text)['result']


# Words to Compare
word1 = 'st'
word2 = 'street'

# Get the word vectors fro each word
vector1 = get_word_vector(word1)
vector2 = get_word_vector(word2)

similarity = 1 - cosine_similarity([vector1], [vector2])
print("Semantic Similarity between " + word1 + " and " + word2 + " is: " + str(similarity[0][0]))



# Use the model
# vector = get_word_vector('example')
# print(vector)