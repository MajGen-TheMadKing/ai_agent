import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    # use argparse to get the arguments passed in when running the command
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    # uv run main.py "user promt here"
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    # uv run main.py "user promt here" --verbose
    # optional
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # get the api key and create a new client using the key
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # messages to be passed into the LLM
    messages = [
        {"role": "user", "content": args.user_prompt},
    ]

    # print the user prompt when --verbose was used
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    # function call to generate an answer from the LLM and print it to the console
    generate_content(client, messages, args.verbose)

 # function to generate an answer from the LLM and print it to the console.
def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:

    # generate a response object by passing in the model to use and the message
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    #error if response usage is not there
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    # what to do when --verbose was used
    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    #always print the response
    print("Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
