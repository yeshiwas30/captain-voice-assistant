import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


# Gemini models used for translation.
# If one is temporarily unavailable, the next one is tried.
MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]


def translate_text(text, target_language="English"):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set in the project .env file"
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
Translate the following text into {target_language}.

Requirements:
- Preserve the original meaning.
- Do not add explanations.
- Do not remove important information.
- Preserve safety instructions and technical terminology.
- Return only the translated text.

Text:
{text}
"""

    last_error = None

    for model in MODELS:

        # Try each model twice
        for attempt in range(2):

            try:
                print(
                    f"Trying translation model: {model} "
                    f"(attempt {attempt + 1}/2)"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0
                    )
                )

                if not response.text:
                    raise RuntimeError(
                        f"Gemini returned an empty translation using {model}"
                    )

                print(
                    f"Translation generated using {model}"
                )

                return response.text.strip()

            except Exception as e:

                last_error = e

                print(
                    f"Translation model {model} failed: "
                    f"{type(e).__name__}: {e}"
                )

                if attempt == 0:
                    print("Waiting 2 seconds before retry...")
                    time.sleep(2)

        print(
            f"Translation model {model} unavailable. "
            f"Trying the next model..."
        )

    raise RuntimeError(
        "All Gemini translation models failed. "
        f"Last error: {last_error}"
    )