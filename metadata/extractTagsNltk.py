## Extract the top 10 most common tags from a document
## This script does not reflect to content in the document

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from collections import Counter
import os   

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

## Set local environment variables
folder_path = "QnA_Examples/content"
file_name = "QnA_Examples/content/state_of_the_union_2023.txt"

# Open the file and read in the contents
with open(file_name, 'r') as f:
    document = f.read()

# Tokenize the document into words
words = word_tokenize(document)

# Remove stop words
stop_words = set(stopwords.words('english'))
words = [word for word in words if word not in stop_words]

# Perform part-of-speech tagging
tagged_words = pos_tag(words)

# Extract the nouns
tags = [word for word, pos in tagged_words if pos in ['NN', 'NNS', 'NNP', 'NNPS']]

# Count the frequency of each tag
tag_counter = Counter(tags)

# Get the 10 most common tags
top_tags = tag_counter.most_common(10)

# Print the top tags
print(top_tags)