import argparse
import os
import json
import sys

from prompts import system_prompt

from call_function import available_functions, call_function

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


    # messages to be passed into the LLM, list of dicts, conversation history
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # print the user prompt when --verbose was used
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    # loop 20 times to let the LLM iterate on its own responses
    for _ in range(20):
        # function call to generate an answer from the LLM and print it to the console
        result = generate_content(client, messages, args.verbose)
        if result:
            print("Final Response:")
            print(result)
            return
    print("Could not finish the task after 20 iterations")
    sys.exit(1)

 # function to generate an answer from the LLM and print it to the console.
def generate_content(client: OpenAI, messages: list, verbose: bool) -> str |None:

    # generate a response object by passing in the model to use and the message
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        #turn temp=0 on when you want the model to behave more consistent, but it comsumes more tokens
        #temperature=0,
    )

    #error if response usage is not there
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    # what to do when --verbose was used
    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    #get the response the LLM gave
    message = response.choices[0].message
    messages.append(message)

    #if the response is a tool call, do it. Otherwise just print the text response
    if message.tool_calls:
        #go through all the tool calls
        for tool_call in message.tool_calls:

            #call the function that the LLM wants to use
            result_of_tool_call = call_function(tool_call, verbose)

            #raise an exception if the result of the tool call has no content
            if not result_of_tool_call["content"]:
                raise Exception("result_of_tool_call is empty")

            messages.append(result_of_tool_call)

            # verbose prints the result of the tool call
            if verbose:
                print(f"-> {result_of_tool_call['content']}")

    else:
        # append and return the text response
        return message.content


if __name__ == "__main__":
    main()
