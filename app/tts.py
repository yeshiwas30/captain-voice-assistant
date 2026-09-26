import os
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


def generate_speech(text):

    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID")

    if not api_key:
        raise RuntimeError(
            "ELEVENLABS_API_KEY is not set in the project .env file"
        )

    if not voice_id:
        raise RuntimeError(
            "ELEVENLABS_VOICE_ID is not set in the project .env file"
        )

    if voice_id.lower() in {
        "your_voice_id",
        "your-voice-id",
        "voice_id"
    }:
        raise RuntimeError(
            "ELEVENLABS_VOICE_ID is still a placeholder. "
            "Replace it with your actual ElevenLabs Voice ID."
        )

    # Clean the text before sending it to TTS
    text = text.strip()

    if not text:
        raise RuntimeError(
            "No text was provided for speech generation."
        )

    url = (
        f"https://api.elevenlabs.io/v1/text-to-speech/"
        f"{voice_id}"
    )

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    data = {
        "text": text,

        # Good multilingual model for Amharic
        "model_id": "eleven_multilingual_v2",

        "voice_settings": {
            # Slightly higher stability helps pronunciation consistency
            "stability": 0.65,

            # Keeps the voice characteristics consistent
            "similarity_boost": 0.85,

            # Adds a little natural expressiveness
            "style": 0.15,

            # More predictable output
            "use_speaker_boost": True
        },

        "output_format": "mp3_44100_128"
    }

    print("Generating Captain's Amharic voice...")

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=90
    )

    if not response.ok:
        print("ElevenLabs error:")
        print(response.text)

    response.raise_for_status()

    static_dir = BASE_DIR / "static"
    static_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = static_dir / "captain_response.mp3"

    with open(output_path, "wb") as audio_file:
        audio_file.write(response.content)

    print(f"Audio saved to: {output_path}")

    return "/static/captain_response.mp3"