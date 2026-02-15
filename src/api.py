"""FastAPI backend for the LLM Reliability Gate."""

import logging
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.config.loader import load_config
from src.orchestrator import build_response, run_workflow

logger = logging.getLogger(__name__)

app = FastAPI(title="LLM Reliability Gate")


class EvaluateRequest(BaseModel):
    config_path: str | None = None


class EvaluateResponse(BaseModel):
    score: float
    decision: str
    total_claims: int
    supported: int
    unsupported: int
    weakly_supported: int
    details: list[dict]


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request: Request, exc: FileNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(request: EvaluateRequest) -> EvaluateResponse:
    request_id = str(uuid4())
    logger.info("request_id=%s Starting evaluation", request_id)

    config = load_config(request.config_path)
    state = {"config": config}
    run_workflow(state)
    result = build_response(state)

    logger.info("request_id=%s Evaluation complete, decision=%s", request_id, result["decision"])
    return EvaluateResponse(**result)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
