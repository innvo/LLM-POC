from flask import Flask, request
from gensim.models import KeyedVectors

app = Flask(__name__)

# Load the model when the server starts
model_path = "./models/GoogleNews-vectors-negative300.bin.gz"
model = KeyedVectors.load_word2vec_format(model_path, binary=True)

@app.route('/use_model', methods=['POST'])
def use_model():
    # Use the model on some data
    data = request.json
    result = model[data['word']]
    return {'result': result.tolist()}

if __name__ == '__main__':
    app.run(port=5000)