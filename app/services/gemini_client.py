from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_TEST_KEY"))

async def ask_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=prompt,
        config={
            "temperature": 0,
            "top_p": 0.8,
            "top_k": 20,
            "max_output_tokens": 200,
        }
    )
    return response.text.strip()