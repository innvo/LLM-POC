import openai

import os
# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

## Set local environment variables
OPENAI_API_KEY=os.getenv("OPEN_API_KEY")

def craft_prompt(topic, examples, num_tokens=100):
  """Constructs prompt to generate text"""
  
  prefix = f"""
  Generate a {num_tokens} word summary on "{topic}".
  The summary should be factual, nuanced, and optimistic. 
  """
  
  examples_text = ""  
  if examples:
    examples_text = "\nExample high quality summaries:\n"
    for ex in examples:
      examples_text += f"\n - {ex}"

  full_prompt = prefix + examples_text + "\n\nSummary:"

  return full_prompt

def generate_text(prompt, engine="text-davinci-003", temp=0.5):
  """Generates text completion from prompt"""

  response = openai.Completion.create(
      engine=engine,
      prompt=prompt,
      max_tokens=300,
      temperature=temp,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
  )

  text = response["choices"][0]["text"].strip()
  
  return text

def score_vagueness(text):
    """Use LLM to analyze vagueness of text"""
    
    prompt = f"On a scale from 0 to 1, score the vagueness level of this text:\n{text}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
    )
    
    # Extract score 
    vagueness_score = float(response.choices[0].text.strip()) 
    
    return vagueness_score


topic = "renewable energy"
examples = [
    # "Solar power converts energy from the Sun into electricity.",
    # "Wind turbines use kinetic energy from wind to generate clean power."
    "I like ice cream"
]
prompt = craft_prompt(topic, examples)

text = generate_text(prompt)
print(text)

print("###################")
print(f"Prompt: {prompt}")
vagueness = score_vagueness(text)
print("###################")
print(f"Vagueness: {vagueness:.3f}")