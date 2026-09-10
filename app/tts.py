import os
import requests


def generate_speech(text):

    api_key = os.getenv(
        "ELEVENLABS_API_KEY"
    )

    voice_id = os.getenv(
        "ELEVENLABS_VOICE_ID"
    )

    url = (
        f"https://api.elevenlabs.io/v1/text-to-speech/"
        f"{voice_id}"
    )

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )

    response.raise_for_status()

    output_path = "static/captain_response.mp3"

    with open(
        output_path,
        "wb"
    ) as audio_file:

        audio_file.write(
            response.content
        )

    return output_path