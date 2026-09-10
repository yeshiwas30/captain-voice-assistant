from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "plots" / ".env")
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.pipeline import (
    initialize_rag,
    run_pipeline
)


app = FastAPI(
    title="Captain Voice Assistant",
    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


class QueryRequest(BaseModel):

    question: str
    target_language: str = "Amharic"


@app.on_event("startup")
def startup():

    initialize_rag()


@app.get("/")
def home():

    return {
        "message":
            "Captain Voice Assistant is running"
    }


@app.post("/ask")
def ask_captain(
    request: QueryRequest
):

    result = run_pipeline(
        request.question,
        request.target_language
    )

    return {

        "question":
            result["input"],

        "retrieved_documents":
            result["retrieved_documents"],

        "answer":
            result["generated_answer"],

        "translation":
            result["translated_answer"],

        "audio":
            "/static/captain_response.mp3",

        "processing_time":
            result["processing_time_seconds"]
    }