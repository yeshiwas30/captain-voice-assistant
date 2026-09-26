import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


# Models are tried in this order.
# If one is temporarily unavailable, the next model is attempted.
MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]


def generate_answer(question, retrieved_documents):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set in the project .env file"
        )

    client = genai.Client(api_key=api_key)

    # Build RAG context
    context = "\n\n".join(
        f"Source: {doc['source']}\n{doc['text']}"
        for doc in retrieved_documents
    )

    prompt = f"""
You are a maritime Captain's assistant.

Answer the Captain's question using ONLY the provided knowledge base.

Rules:
- Do not invent information.
- Do not invent procedures, numbers, limits, or safety instructions.
- If the knowledge base does not contain enough information, say:
  "I don't have enough information in the knowledge base."
- Mention the relevant source document.
- Keep the answer clear and concise.

Knowledge Base:
{context}

Captain's Question:
{question}
"""

    last_error = None

    for model in MODELS:

        # Try each model up to 2 times
        for attempt in range(2):

            try:
                print(
                    f"Trying Gemini model: {model} "
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
                        f"Gemini returned an empty response using {model}"
                    )

                print(f"Gemini response generated using {model}")

                return response.text

            except Exception as e:

                last_error = e

                print(
                    f"Gemini model {model} failed: "
                    f"{type(e).__name__}: {e}"
                )

                # Wait before retrying
                if attempt == 0:
                    print("Waiting 2 seconds before retry...")
                    time.sleep(2)

        print(
            f"Model {model} unavailable. "
            f"Trying the next model..."
        )

    raise RuntimeError(
        "All Gemini models failed. "
        f"Last error: {last_error}"
    )