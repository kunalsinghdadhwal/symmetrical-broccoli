"""AWS Bedrock wrapper -- single point of contact with AWS Bedrock."""

import json
import os

import boto3

_client = boto3.client(
    "bedrock-runtime",
    region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
)


def call_llm(prompt: str, system: str = "") -> str:
    """Call Claude via the Converse API and return the assistant text."""
    model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

    kwargs: dict = {
        "modelId": model_id,
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"maxTokens": 4096, "temperature": 0.0},
    }

    if system:
        kwargs["system"] = [{"text": system}]

    response = _client.converse(**kwargs)
    return response["output"]["message"]["content"][0]["text"]  # type: ignore[no-any-return]


def embed(text: str) -> list[float]:
    """Generate an embedding vector via Titan."""
    model_id = os.environ.get("TITAN_MODEL_ID", "amazon.titan-embed-text-v2:0")

    response = _client.invoke_model(
        modelId=model_id,
        body=json.dumps({"inputText": text}),
        accept="application/json",
        contentType="application/json",
    )
    return json.loads(response["body"].read())["embedding"]  # type: ignore[no-any-return]
