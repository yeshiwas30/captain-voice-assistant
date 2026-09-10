import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_answer(question, retrieved_documents):

    context = "\n\n".join(
        [
            f"Source: {doc['source']}\n"
            f"{doc['text']}"
            for doc in retrieved_documents
        ]
    )

    prompt = f"""
You are a maritime Captain's assistant.

Answer the Captain's question using ONLY the
provided knowledge base.

If the knowledge base does not contain enough
information to answer the question, say:

"I don't have enough information in the knowledge base."

Do not invent procedures, limits, numbers,
or safety instructions.

Always mention the relevant source documents.

Knowledge Base:
{context}

Captain's Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a precise maritime assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content