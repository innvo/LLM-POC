import  datetime
import openai
import re

openai.api_key = "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"

timeframe_pattern = r"\b(?:last year|hour|minute|second|am|pm|midnight|noon|midday|morning|afternoon|evening|night|day|week|month|year|decade|century|millennium|today|yesterday|tomorrow|next|last|previous|upcoming|soon|later|now|then|since|until|during|throughout|for|within|recently|lately|previously|initially|originally|eventually|subsequently|presently|currently|presently|temporarily|permanently|briefly|momentarily|instantaneously|eventually|subsequently|earlier|later|before|after|afterward|ahead|behind|beforehand|promptly|immediately|quickly|shortly|presently|currently|ongoing|continuous|continual|intermittent|periodic|occasional|frequent|regular|irregular|sporadic|seldom|rarely|never|always|Christmas|New Year's|Thanksgiving|birthday|anniversary|weekend|holiday|summer|winter|spring|fall|daily|weekly|monthly|yearly|annually|bi-weekly|quarterly|semi-annually|once|twice|thrice|several times|often|frequently|regularly|rarely|seldom|never|always|a few minutes|a couple of hours|a few days|a week or two|a month or so|a year or two|1|2|3|4|5|6|7|8|9|10|00|30|60|one|two|three|four|five|six|seven|eight|nine|ten|hrs|mins|secs|wk|mth|yr|right now|ASAP|immediately|shortly|pretty soon|in a bit|in a while|a while back|ages ago|the other day|the other week|the other month|the other year |last year) | \b"

text = "what did the president Biden say about the southern border in the state union address in 2022  "

response_about = openai.Completion.create(
  engine="gpt-3.5-turbo-instruct",
  prompt=f"Extract the entity that is tied to the 'about' from this question:\n\n{text}\n\nabout:",
  temperature=0,
  max_tokens=255,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

about = response_about["choices"][0]["text"].strip()
print("about:", about)

response_what = openai.Completion.create(
  engine="gpt-3.5-turbo-instruct",
  prompt=f"Extract the entity that is tied to the 'what' from this question:\n\n{text}\n\nwhat:",
  temperature=0,
  max_tokens=60,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

what = response_what["choices"][0]["text"].strip()
print("what:",what)

response_who = openai.Completion.create(
  engine="gpt-3.5-turbo-instruct",
  prompt=f"Extract the entity that is tied to the 'who' from this question:\n\n{text}\n\nwho:",
  temperature=0,
  max_tokens=60,
  top_p=1   ,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

who = response_who["choices"][0]["text"].strip()
print("who:", who)

response_when= openai.Completion.create(
  engine="gpt-3.5-turbo-instruct",
  prompt=f"Extract the timeframe that is tied to this question:\n\n{text}:",
  temperature=0.8,
  max_tokens=60,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

when_text = response_when["choices"][0]["text"].strip()

# Check for valid time expressions using a regular expression
timeframe_match = re.search(timeframe_pattern, when_text)

if timeframe_match  is None:
    timeframe = 'Not Provided'

if timeframe_match and timeframe_match.group() == "last year":
    current_year = datetime.datetime.now().year
    timeframe = current_year - 1  # Calculate last year
# else:
    # timeframe = timeframe_match.group() if timeframe_match else when_text

print("when text:", when_text)
print("timeframe_match", timeframe_match)
print("timeframe", timeframe)