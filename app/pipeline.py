import json
import os
from datetime import datetime

from app.rag import RAGRetriever
from app.llm import generate_answer
from app.translator import translate_text
from app.tts import generate_speech


rag = RAGRetriever()


def initialize_rag():

    try:
        rag.load_index()

        print("Existing FAISS index loaded.")

    except Exception:

        print("Building FAISS index...")

        rag.load_documents()
        rag.build_index()


def run_pipeline(
    question,
    target_language="Amharic"
):

    start_time = datetime.now()

    # -----------------------------
    # STEP 1: RETRIEVAL
    # -----------------------------

    retrieved_documents = rag.retrieve(
        question,
        top_k=3
    )

    # -----------------------------
    # STEP 2: LLM
    # -----------------------------

    answer = generate_answer(
        question,
        retrieved_documents
    )

    # -----------------------------
    # STEP 3: TRANSLATION
    # -----------------------------

    translated = translate_text(
        answer,
        target_language
    )

    # -----------------------------
    # STEP 4: TTS
    # -----------------------------

    audio_path = generate_speech(
        translated
    )

    end_time = datetime.now()

    trace = {

        "timestamp":
            start_time.isoformat(),

        "input":
            question,

        "retrieved_documents":
            retrieved_documents,

        "generated_answer":
            answer,

        "translated_answer":
            translated,

        "audio":
            audio_path,

        "processing_time_seconds":
            (
                end_time - start_time
            ).total_seconds()
    }

    os.makedirs(
        "logs",
        exist_ok=True
    )

    with open(
        "logs/pipeline.jsonl",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                trace,
                ensure_ascii=False
            ) + "\n"
        )

    return trace