import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function, available_functions


load_dotenv("geminitest.env")
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# No cli argument provided
if len(sys.argv) < 2:
    sys.exit(1)

# store user input and gemini response to prompt
user_input = sys.argv[1]
system_prompt = '''
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
Do NOT EVER create a file unless explicitly requested by the user.

- When searching for file specified by user, use get_files_info to list out what is a directory or file.
- If file relative to user query is not found in list info of current directory, search for next directory labeled in list as 'is_dir=True' in stats.
- Search the next directory for applicable file.
- When applicable file is found, read file contents with get_file_content to base your response on.

'''

args = []
for arg in sys.argv[1:]:
    if not arg.startswith("--"):
        args.append(arg)

if not args:
    print('\nUsage: python main.py "your prompt here" [--verbose]')
    sys.exit(1)

user_input = " ".join(args)

messages = [types.Content(role="user", parts=[types.Part(text=user_input)]),]

for i in range(0, 20):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )

    for candidate in response.candidates:
        try:
            messages.append(candidate.content)
        except:
            raise Exception("Fatal Exception: check candidate did not produce expected result")

    verbose = False
    # optional verbose flag for extra info
    if "--verbose" in sys.argv:
        verbose = True
        print(f'User prompt: {user_input}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
        print("\n")

    if response.function_calls:
        for calls in response.function_calls:
            result = call_function(calls, verbose)
            messages.append(types.Content(role="user", parts=result.parts))
        continue
    
    try:
        if verbose == True:
            print(f"-> {result.parts[0].function_response}")
    except:
        raise Exception("Fatal Exception: call_function args did not produce expected result")

    if response.text:
        print("Final response:")
        print(response.text.strip())
        break
    continue