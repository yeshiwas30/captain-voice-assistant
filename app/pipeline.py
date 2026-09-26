
import json
import os
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

from app.rag import RAGRetriever
from app.llm import generate_answer
from app.translator import translate_text
from app.tts import generate_speech


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from:
# D:\project\captain-voice-assistant\.env
load_dotenv(BASE_DIR / ".env", override=True)


# ============================================================
# RAG
# ============================================================

rag = RAGRetriever()


def initialize_rag():

    try:
        rag.load_index()

        print("Existing FAISS index loaded.")

    except Exception as e:

        print("Building FAISS index...")
        print(f"Reason: {e}")

        rag.load_documents()
        rag.build_index()


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_pipeline(
    question,
    target_language="Amharic"
):

    start_time = datetime.now()

    # --------------------------------------------------------
    # STEP 1: RETRIEVAL
    # --------------------------------------------------------

    print("\n[1/4] Retrieving relevant knowledge...")

    retrieved_documents = rag.retrieve(
        question,
        top_k=3
    )

    print(
        f"Retrieved {len(retrieved_documents)} documents."
    )

    # --------------------------------------------------------
    # STEP 2: LLM
    # --------------------------------------------------------

    print("[2/4] Generating answer with Gemini...")

    answer = generate_answer(
        question,
        retrieved_documents
    )

    print("Gemini answer generated.")

    # --------------------------------------------------------
    # STEP 3: TRANSLATION
    # --------------------------------------------------------

    print(
        f"[3/4] Translating answer to {target_language}..."
    )

    translated = translate_text(
        answer,
        target_language
    )

    print("Translation completed.")

    # --------------------------------------------------------
    # STEP 4: TEXT-TO-SPEECH
    # --------------------------------------------------------

    print("[4/4] Generating speech...")

    audio_path = generate_speech(
        translated
    )

    print("Speech generated.")

    # --------------------------------------------------------
    # PROCESSING TIME
    # --------------------------------------------------------

    end_time = datetime.now()

    processing_time = (
        end_time - start_time
    ).total_seconds()

    # --------------------------------------------------------
    # PIPELINE TRACE
    # --------------------------------------------------------

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
            processing_time
    }

    # --------------------------------------------------------
    # SAVE LOG
    # --------------------------------------------------------

    logs_dir = BASE_DIR / "logs"

    logs_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    log_file = logs_dir / "pipeline.jsonl"

    with open(
        log_file,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                trace,
                ensure_ascii=False
            ) + "\n"
        )

    print(
        f"Pipeline completed in {processing_time:.2f} seconds."
    )

    return trace

