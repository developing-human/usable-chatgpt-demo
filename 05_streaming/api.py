import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Iterator
from openai import OpenAI

class Suggestion(BaseModel):
    label: str
    description: str

# Uses ChatGPT to offer troubleshooting suggestions based on sound & location
def troubleshoot_car(sound: str, location: str) -> Iterator[Suggestion]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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
    # Receives back an Iterator of responses, each with a few characters
    # of the response wrapped in JSON.
    response_stream = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
    stream=True)
        
    # Extracts the text content from the response.
    chunks = (extract_content(r) for r in response_stream)
    
    # Parses the response into Suggestions and returns them
    return parse_suggestions(chunks)

def extract_content(gpt_response):
    return gpt_response.choices[0].delta.content or ""


# Parses ChatGPT's response into a list of suggestions
def parse_suggestions(chunks: Iterator[str]) -> Iterator[Suggestion]:
    for line in to_lines(chunks):
        # Label? Extract the text and store it.
        if line.startswith("label:"):
            label = line.split(":")[1].strip()

        # Description? Extract the text, create suggestion.
        elif line.startswith("description:"):
            description = line.split(":")[1].strip()
            yield Suggestion(label=label, description=description)


# Takes an iterator over small strings
# Returns an iterator over lines
def to_lines(chunks: Iterator[str]) -> Iterator[str]:
    current_line = ""

    for chunk in chunks:
        if chunk is None:
            continue

        if "\n" in chunk:
            # Chunk has newline, split into multiple lines
            lines = chunk.split("\n")

            # Part before the newline is part of current line
            current_line += lines[0]

            # Got an entire line, emit it, reset it
            yield current_line
            current_line = ""

            # If there is a part after the newline, 
            # store it as a new current_line
            if len(lines) > 1:
                current_line = lines[1]
        else:
            # No newline, add to current line
            current_line += chunk

    # Yield any remaining incomplete line after the loop
    if current_line:
        yield current_line


def create_app() -> FastAPI:
    app = FastAPI()

    @app.websocket("/search")
    async def search(websocket: WebSocket, sound: str, location: str) -> list[Suggestion]:
        await websocket.accept()
        for suggestion in troubleshoot_car(sound, location):
            print(f"Sending a suggestion: {suggestion.model_dump_json()}")
            await websocket.send_text(suggestion.model_dump_json())

        await websocket.close()

    return app

# Exit early if the api key is not provided
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
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

