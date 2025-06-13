import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file


try:
    user_prompt = sys.argv[1]
except IndexError:
    print("A prompt must be provided in order to generate a response.")
    sys.exit(1)

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
CLIENT = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash-001"
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
    ]
)
generated_content = CLIENT.models.generate_content(
    model=MODEL,
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=SYSTEM_PROMPT
    ),
)

if generated_content.function_calls is not None:
    for function_call_part in generated_content.function_calls:
        function_call_result = call_function(function_call_part)
        response = function_call_result.parts[0].function_response.response

        if response is None:
            raise Exception("A response couldn't be generated based on your request.")

        if "--verbose" in sys.argv:
            print(f"-> {function_call_result.parts[0].function_response.response}")

print(generated_content.text)

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")

    if generated_content.usage_metadata is not None:
        print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}")
        print(
            f"Response tokens: {generated_content.usage_metadata.candidates_token_count}"
        )
