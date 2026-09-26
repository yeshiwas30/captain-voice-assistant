# Captain Voice Assistant with RAG-Based Translation

An AI-powered maritime assistant that uses **RAG (Retrieval-Augmented Generation)** to answer Captain's questions using a maritime knowledge base, translate responses into languages such as **Amharic**, and generate voice responses.

## Features

* 📚 RAG-based maritime knowledge retrieval using **FAISS**
* 🤖 Grounded responses using **Google Gemini**
* 🌍 Multilingual translation
* 🗣️ Voice generation using **ElevenLabs**
* 🔊 Audio response playback
* 📝 Pipeline logging and traceability
* ⚡ FastAPI backend with web interface

## Technologies

* Python
* FastAPI
* FAISS
* Sentence Transformers
* Google Gemini
* ElevenLabs
* HTML / JavaScript

## Project Flow

```text
Captain Question
      ↓
FAISS RAG Retrieval
      ↓
Gemini Answer
      ↓
Translation
      ↓
ElevenLabs TTS
      ↓
Voice Response
```

## Setup

```powershell
git clone https://github.com/yeshiwas30/captain-voice-assistant.git
cd captain-voice-assistant

python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```text
GEMINI_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=your_voice_id
```

Build the RAG index:

```powershell
python -m scripts.build_index
```

Run the application:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Example

**Question:**

> What should I do if there is a fire onboard?

The system retrieves relevant maritime information, generates a grounded answer, translates it into Amharic, and produces a voice response.

## Note

This is an educational prototype. AI responses should be verified against vessel-specific procedures, official maritime regulations, and qualified personnel before operational use.
