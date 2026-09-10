# Captain Voice Assistant with RAG-Based Translation

## Overview

Captain Voice Assistant is an AI-powered maritime assistant that uses **RAG (Retrieval-Augmented Generation)** to retrieve relevant information from a maritime knowledge base and generate grounded responses.

The response can be translated into a selected language, such as **Amharic**, and converted into speech.

## Technologies

* Python & FastAPI
* FAISS Vector Database
* Sentence Transformers
* Ollama (Llama 3.2 3B)
* Translation
* Text-to-Speech
* HTML, CSS & JavaScript

## Architecture

text
Captain Question
      ↓
   FastAPI
      ↓
   FAISS RAG
      ↓
 Ollama LLM
      ↓
 Translation
      ↓
 Text-to-Speech
      ↓
 Audio Response


## Setup

powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt


Install and start Ollama:

powershell
ollama pull llama3.2:3b
ollama serve


Build the knowledge-base index:

powershell
python -m scripts.build_index


Run the application:

powershell
python -m uvicorn app.main:app --reload


Open:
text
http://127.0.0.1:8000/static/index.html


## Knowledge Base

The system uses maritime documents covering areas such as:

* Safety
* Navigation
* Fire procedures
* Weather
* Engine room
* Maintenance
* Crew operations

## Evaluation

Run:

powershell
python -m scripts.evaluate


The system logs the complete pipeline:

text
Input → Retrieved Context → LLM Response → Translation → Audio

 Limitations

This is a prototype for demonstration purposes. It should not replace official maritime procedures, vessel SMS, manufacturer manuals, or applicable regulations.
