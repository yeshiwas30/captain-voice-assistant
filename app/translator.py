import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def translate_text(
    text,
    target_language="Amharic"
):

    prompt = f"""
Translate the following maritime assistant response
into {target_language}.

Requirements:

- Preserve the meaning exactly.
- Do not add information.
- Do not remove safety instructions.
- Preserve numbers and measurements.
- Keep technical maritime terminology accurate.

Text:

{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a professional technical translator."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content