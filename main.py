import os
import sys
from config import *
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 main.py <prompt> --verbose(optional)")
        sys.exit(1)

    prompt = sys.argv[1]
    verbose = False
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(f"Missing API key")
        exit(1)
    client = genai.Client(api_key=api_key)

    if verbose:
        print(f"User prompt: {prompt}")

    for i in range(ITER_CAP):
        try:
            content = client.models.generate_content(model="gemini-2.0-flash-001", 
                                                    contents=messages,
                                                    config=types.GenerateContentConfig(tools=[available_functions],
                                                                                        system_instruction=system_prompt))

            if content.candidates:
                for can in content.candidates:
                    messages.append(can.content)
            
            if not content.function_calls:
                print(content.text)
                break

            response_parts = []
            for function_call_part in content.function_calls:
                function_results = call_function(function_call_part, verbose)
                if not function_results.parts:
                    raise Exception("No function responses generated, exiting.")
                if not function_results.parts[0].function_response.response:
                    raise Exception("Fatal Exception: Unexpected function result")
                if verbose:
                    print(f"-> {function_results.parts[0].function_response.response}")
                response_parts.append(function_results.parts[0])

            new_message = types.Content(role="user", parts=response_parts)
            messages.append(new_message)
            
            if i == ITER_CAP - 1:
                print(f"Maximum {ITER_CAP} iterations reached.")
                sys.exit(1)

        except Exception as e:
            print(f"Error: {e}")
            exit(1)

        if verbose and content.usage_metadata:
            print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {content.usage_metadata.candidates_token_count}")


main()