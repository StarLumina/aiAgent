import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    list_of_results=[]

    response = client.models.generate_content(
        model = 'gemini-2.5-flash', 
        contents = messages,
        config = types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            )
        )
    if response.usage_metadata is None:
        raise RuntimeError("NO METADATA")
    
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts: raise Exception("Error: missing parts field from function call result")
            if function_call_result.parts[0].function_response == None: raise Exception("Error: missing response")
            if function_call_result.parts[0].function_response.response == None: raise Exception("Error: missing response field from response")
            list_of_results.append(function_call_result.parts[0])
            if verbose: print(f"-> {function_call_result.parts[0].function_response.response}")


    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
    else:
        print(f"\n{response.text}")



if __name__ == "__main__":
    main()
