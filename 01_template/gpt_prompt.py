import os
import sys

def do_the_thing(arg1: str, arg2: str) -> str:
    prompt = f"""Dear ChatGPT, 

    Please do the thing with {arg1} and {arg2}.

    Forever yours,
    A Human
    """

    # TODO: Call ChatGPT with the prompt.

    return "TODO: Set this to content of the ChatGPT response"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 gpt_prompt.py arg1 arg2")
        exit(1)

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        print("Must define environment variable OPENAI_API_KEY")
        exit(1)

    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    # Print the ChatGPT response
    response = do_the_thing(arg1, arg2)
    print(response)

