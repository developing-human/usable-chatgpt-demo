import openai
import os
import sys
import json

class Suggestion:
    def __init__(self, label, description):
        self.label = label
        self.desription = description


# Uses ChatGPT to offer troubleshooting suggestions based on sound & location
def troubleshoot_car(sound: str, location: str) -> list[Suggestion]:
    prompt = f"""Your goal is to help me troubleshoot a problem with my car.  I'm hearing a {sound} near {location}.  Suggest 3 ideas for determining the issue.

Please format your response like:
label: Brief label for this section
description: Describe what the problem may be and how to confirm it

For example:
label: Worn Serpentine Belt
description: 40-50 words describing what the issue may be

label: Tensioner Pulley
description: 40-50 words describing what the issue may be
"""

    # Calls ChatGPT 3.5 with the above prompt.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
        
    # Extracts the text content from the response.
    response_content = response.choices[0].message["content"]

    # Parses the response into Suggestions and returns them
    return parse_suggestions(response_content)


# Parses ChatGPT's response into a list of suggestions
def parse_suggestions(text: str) -> list[Suggestion]:
    suggestions = []
    lines = text.strip().split('\n')

    for line in lines:
        if line.startswith("label:"):
            label = line.split(":")[1].strip()
        elif line.startswith("description:"):
            description = line.split(":")[1].strip()
            suggestion = Suggestion(label, description)
            suggestions.append(suggestion)

    return suggestions

# Exit early if incorrect arguments were provided
if len(sys.argv) != 3:
    print("Usage: python3 gpt_prompt.py sound location")
    exit(1)

# Exit early if the api key is not provided
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    print("Must define environment variable OPENAI_API_KEY")
    exit(1)

sound = sys.argv[1]
location = sys.argv[2]

suggestions = troubleshoot_car(sound, location)
print(json.dumps([s.__dict__ for s in suggestions]))

