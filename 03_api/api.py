import openai
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Suggestion(BaseModel):
    label: str
    description: str

# Uses ChatGPT to offer troubleshooting suggestions based on sound & location
def troubleshoot_car(sound: str, location: str) -> list[Suggestion]:
    prompt = f"""Your goal is to help me troubleshoot a problem with my car.  
I'm hearing a {sound} near {location}.  
Suggest 3 ideas for determining the issue.

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

    # Split the response into lines
    lines = text.strip().split('\n')

    for line in lines:
        # Label? Extract the text and store it.
        if line.startswith("label:"):
            label = line.split(":")[1].strip()

        # Description? Extract the text, create suggestion.
        elif line.startswith("description:"):
            description = line.split(":")[1].strip()
            suggestion = Suggestion(label=label, description=description)
            suggestions.append(suggestion)

    return suggestions

def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/search")
    def search(sound: str, location: str) -> list[Suggestion]:
        return troubleshoot_car(sound, location)

    return app

# Exit early if the api key is not provided
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    print("Must define environment variable OPENAI_API_KEY")
    exit(1)

app = create_app()

# TODO: Very permissive CORS for development!  
# TODO: In a production application, make this more restrictive.
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

