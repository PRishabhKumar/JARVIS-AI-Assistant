# First install the SDK:
# pip install google-genai

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def query_gemini(prompt: str):
    # Create client with your API key
    client = genai.Client(api_key=os.getenv("geminiAPI"))

    # Send a generation request
    response = client.models.generate_content(
        model="gemini-2.5-flash",       # choose the model you have access to
        contents=prompt                 # the prompt text
    )

    # Print the output
    print("Response text:", response.text)

if __name__ == "__main__":
    my_prompt = "Explain how a neural network works in simple terms."
    print("Sending request")
    query_gemini(my_prompt)
