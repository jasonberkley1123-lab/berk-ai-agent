import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("no api key found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

def main():
    for _ in range(20):
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        if response.candidates:
            for cand in response.candidates:
                if cand.content:
                    messages.append(cand.content)
        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                result = call_function(function_call, args.verbose)
                if not result.parts:
                    raise RuntimeError("error")
                if result.parts[0].function_response == None:
                    raise RuntimeError("error")
                if result.parts[0].function_response.response == None:
                    raise RuntimeError("error")
                function_responses.append(result.parts[0])
                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            if response.usage_metadata == None:
                raise RuntimeError("no data exists")
            if not args.verbose:
                print(response.text)
                break
            else:
                print("User prompt:", args.user_prompt)
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
                print(response.text)
                break
    else:
        print("Reached max iterations without a final response")
        raise SystemExit(1)

if __name__ == "__main__":
    main()