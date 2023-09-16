import openai
import os
import sys
import json
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Iterator

class Suggestion(BaseModel):
    label: str
    description_delta: str

# Uses ChatGPT to offer troubleshooting suggestions based on sound & location
def troubleshoot_car(sound: str, location: str) -> Iterator[Suggestion]:
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
    response_chunks = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
        
    # Extracts the text content from the response.
    chunks = (rc.choices[0].get("delta", {}).get("content") for rc in response_chunks)

    # Parses the response into Suggestions and returns them
    return parse_suggestions(chunks)


# Parses ChatGPT's response into a list of suggestions
def parse_suggestions(chunks: Iterator[str]) -> Iterator[Suggestion]:
    current_line = ""
    current_label = None
    sent_description = ""

    for chunk in chunks:
        if chunk is None:
            continue

        # The chunk may or may not have a newline in it.  Only use the part before
        # the newline for now.
        lines = chunk.split("\n")
        current_line += lines[0]

        if current_line.startswith("label:") and len(lines) > 1:
            # We have the entire label, so add it to the suggestion.
            current_label = current_line.split(":")[1].strip()

        elif current_line.startswith("description:"):
            # Calculate the part of the description we haven't sent yet.
            description = current_line.split(":")[1].strip()
            description_delta = description.replace(sent_description, "")
            sent_description = description

            yield Suggestion(label=current_label, description_delta=description_delta)


        # If this chunk spanned two lines, keep the second line
        if len(lines) > 1:
            current_line = lines[1]


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/search")
    def search(sound: str, location: str) -> list[Suggestion]:
        return troubleshoot_car(sound, location)

    @app.websocket("/ws")
    async def search(websocket: WebSocket, sound: str, location: str) -> list[Suggestion]:
        print(f"Before accept: {sound} {location}")
        await websocket.accept()
        print("After accept")
        for suggestion in troubleshoot_car(sound, location):
            await websocket.send_text(suggestion.json())

        await websocket.close()

    return app

# Exit early if the api key is not provided
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    print("Must define environment variable OPENAI_API_KEY")
    exit(1)

app = create_app()

# Very permissive CORS for development!  
# In a real production application, make this much more restrictive.
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)
