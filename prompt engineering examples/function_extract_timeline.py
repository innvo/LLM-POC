import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_md")

# Example text
text = "What did President Biden say about the southern border in the state union address in 2022?"
text = "What did President Biden say about the southern border yesterday?"
text = "What did President Biden say about the southern border?"
text = "What did President Biden say last year?"
text = "What did President Biden say?"
text = "Where did eric live over the past 10 years?"
# Process the text with SpaCy
doc = nlp(text)

# Extract dates or timeframes
timeframes = [ent.text for ent in doc.ents if ent.label_ in ["DATE", "TIME"]]

print(timeframes)