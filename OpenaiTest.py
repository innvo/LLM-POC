from langchain.document_loaders import TextLoader

import openai
openai.api_key = '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'

response = openai.Completion.create(
    engine="text-davinci-002",
    prompt="Write a poem about a cat",
    temperature=0.7,
    max_tokens=100,
)

print(response.choices[0].text)