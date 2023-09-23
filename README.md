The goal of this project is to provide a straight forward example for building
a FastAPI + React application which streams semi-structured responses to the
front end.

As an example it walks through an application which helps a person troubleshoot
an issue with their car based on the sound it's making and where it's coming
from.

### Setup

```
# Create a virtualenv for this project
python3 -m venv venv

# Activate the virtualenv
# Note: when done, deactivate the venv with: deactivate
source venv/bin/active

# uvicorn lets us run the FastAPI application
pip3 install uvicorn

pip3 install -r requirements
```

### Organization

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

### Tools

- **uvicorn** for running the FastAPI server
- **jq** for formatting JSON on command line
- **curl** to test calling ChatGPT and JSON API
