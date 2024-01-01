import spacy

# Specify to use CPU explicitly
spacy.prefer_gpu = True

# Load the English NLP model
nlp = spacy.load("en_core_web_md")  # Load the English NLP model

import spacy

def extract_question_words(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    about = None
    who = None
    what = None 
    when = None
    why = None
    
    for token in doc:
        if token.dep_ == "nsubj" or token.dep_ == "attr":
            who = token.text
        if token.dep_ == "ROOT":
            what = token.text
        if token.dep_ == "advmod":
            when = token.text 
        if token.dep_ == "advcl":
            why = token.text
            
    return {"about": about,
            "who": who, 
            "what": what,
            "when": when,
            "why": why}

text = "what did the president say about the southern border"
print(extract_question_words(text))