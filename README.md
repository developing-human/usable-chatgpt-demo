The goal of this project is to provide a straight forward example for building
a FastAPI + React application which streams semi-structured responses to the
front end.

As an example it walks through an application which helps a person troubleshoot
an issue with their car based on the sound it's making and where it's coming
from.

### Organization

- **00_curl** shows how to call the ChatGPT API with curl.
- **01_template** provides a basic template for accepting the command line
  arguments we'll want for later steps.
- **02_script** starts building the demo as a script which accepts command
  line arguments and constructs a ChatGPT request with those arguments. It
  prints the response to the screen.
- **03_api** uses FastAPI to replace our command line interface with a JSON
  API we can call with `curl`.
- **04_frontend** adds a basic React frontend which prompts for inputs and
  calls the JSON API.
- **05_streaming** streams the individual suggestions as they come back from
  ChatGPT in their entirety.
- **06_smooth_streaming** streams text token-by-token to the front end as it
  comes back from ChatGPT

### Setup

#### Get an OpenAI key
Go to [OpenAI](https://platform.openai.com/signup) to pay for an OpenAI key

Rename `.env.example` to `.env`
```
mv .env.example .env
```

Finally, add your custom OpenAI API key in quotes in that `.env` file
```
OPENAI_API_KEY="fake-api-key-oisAiH29375iH2k3j5lKh"

```


#### Create a virtual environment
```
# Create a virtualenv for this project
python3 -m venv venv

# Activate the virtualenv
# Note: when done, deactivate the venv with: deactivate
source venv/bin/active
```
#### Install remaining Python dependencies
```
# uvicorn lets us run the FastAPI application
pip3 install uvicorn

pip3 install -r requirements.txt
```


### Running examples
- Change into directory for phase of project you're working with
- Starting with step 3, start the python backend with `uvicorn api:app --reload`
- (For 4-6) run `npm install` then `npm run dev`


### Tools

- **uvicorn** for running the FastAPI server
- **jq** for formatting JSON on command line
- **curl** to test calling ChatGPT and JSON API
