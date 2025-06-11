import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.0-flash-001"

try:
    prompt = sys.argv[1]
except IndexError:
    print("A prompt must be provided in order to generate a response.")
    sys.exit(1)

response = client.models.generate_content(
    model=model,
    contents=prompt,
)

print(response.text)

if response.usage_metadata is not None:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
