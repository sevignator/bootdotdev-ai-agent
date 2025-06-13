import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

try:
    user_prompt = sys.argv[1]
except IndexError:
    print("A prompt must be provided in order to generate a response.")
    sys.exit(1)

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.0-flash-001"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

response = client.models.generate_content(
    model=model,
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

if response.function_calls is not None:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(response.text)

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")

    if response.usage_metadata is not None and "--verbose" in sys.argv:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
