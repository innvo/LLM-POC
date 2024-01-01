import re

def score_vagueness(prompt):
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

# Example usage:
prompt1 = "What did the President say?"
prompt2 = "What did President Biden say in his 2023 state of the union address?"

score1 = score_vagueness(prompt1)
score2 = score_vagueness(prompt2)

print("Vagueness score for prompt 1:", score1)
print("Vagueness score for prompt 2:", score2)