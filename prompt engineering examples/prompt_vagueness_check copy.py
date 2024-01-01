import re
import os
import openai
# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

## Set local environment variables
OPENAI_API_KEY=os.getenv("OPEN_API_KEY")



def score_vagueness_rules(prompt):
    """Scores the vagueness of a prompt on a scale of 0 to 1, with 1 being the most specific.

    Args:
        prompt (str): The prompt to score.

    Returns:
        float: The normalized vagueness score, where 1 is very specific and 0 is very vague.
    """

    score = 0

    # Check for specific names, dates, and events:
    if not re.search(r"\b\w+\b", prompt):
        score += 2  # No proper nouns
    if not re.search(r"\d{4}", prompt):
        score += 1  # No years
    if not re.search(r"\bevent\b|\bspeech\b|\bstatement\b|\baddress\b", prompt):
        score += 1  # No explicit event indicators

    # Check for vague terms:
    vague_terms = ["something", "anything", "someone", "anyone", "some", "any",
                    "thing", "things", "stuff", "a lot", "many", "few", "little",
                    "good", "bad", "big", "small"]
    if any(term in prompt.lower() for term in vague_terms):
        score += 1

    # Check for question words:
    question_words = ["who", "what", "when", "where", "why", "how"]
    if any(word in prompt.lower() for word in question_words):
        score -= 1  # Questions tend to be more specific

    # Check for length:
    if len(prompt.split()) < 5:
        score += 1  # Shorter prompts often lack detail

    # Normalize the score to the 0-1 range:
    score = max(0, min(score, 5))
    score = 1 - (score / 5)

    return score

def score_vagueness_llm(prompt):
    """Prompts the OpenAI LLM to assess prompt vagueness and extracts a score."""

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"On a scale of 0 to 1, with 1 being very specific and 0 being very vague, how vague is this prompt: {prompt}?",
        max_tokens=255,
        n=1,
        stop=None,
        temperature=0.7,
    )
    response_text = response.choices[0].text
    vagueness_score_str = response.choices[0].text.strip()
    #print(response_text)
    print(vagueness_score_str)

    try:
        vagueness_score_llm = float(vagueness_score_str)
    except ValueError:
        print(f"OpenAI failed to provide a numerical score: {vagueness_score_str}")
        vagueness_score_llm = 0.5  # Assign a default score

    return vagueness_score_llm

def combined_vagueness_score(prompt):
    """Calculates a combined vagueness score using both rule-based and LLM-based methods."""

    score_rules = score_vagueness_rules(prompt)
    score_llm = score_vagueness_llm(prompt)

    combined_score = (score_rules + score_llm) / 2

    return combined_score
# Example usage:
prompt2 = "What did the President Biden say about the Southern Border?"
#prompt2 = "What did President Biden say in his 2023 state of the union address?"

#combined_score1 = combined_vagueness_score(prompt1)
#combined_score2 = combined_vagueness_score(prompt2)
#llm_score1 = score_vagueness_llm(prompt1)
llm_score2 = score_vagueness_llm(prompt2)
# print("Combined vagueness score for prompt 1:", combined_score1, "LLM score:", llm_score1)
# print("Combined vagueness score for prompt 2:", combined_score2, 'LLM score:', llm_score2)
#print("LLM vagueness score for prompt 1:", llm_score1)
print("LLM vagueness score for prompt 2:", llm_score2)