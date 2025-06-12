import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

try:
    user_prompt = sys.argv[1]
except IndexError:
    print("A prompt must be provided in order to generate a response.")
    sys.exit(1)

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.0-flash-001"
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

response = client.models.generate_content(
    model=model,
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

print(response.text)

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")

    if response.usage_metadata is not None and "--verbose" in sys.argv:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
