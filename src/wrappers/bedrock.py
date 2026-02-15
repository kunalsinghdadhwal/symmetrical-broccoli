"""AWS Bedrock wrapper -- single point of contact with AWS Bedrock."""

import json
import os

import boto3

_client = boto3.client(
    "bedrock-runtime",
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
)


def call_llm(prompt: str, system: str = "") -> str:
    """Call Claude via invoke_model and return the assistant text."""
    model_id = os.environ.get(
        "BEDROCK_INFERENCE_PROFILE_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
    )

    body: dict = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0,
    }

    if system:
        body["system"] = system

    response = _client.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]  # type: ignore[no-any-return]


def embed(text: str) -> list[float]:
    """Generate an embedding vector via Titan."""
    model_id = os.environ.get("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")

    response = _client.invoke_model(
        modelId=model_id,
        body=json.dumps({"inputText": text}),
        accept="application/json",
        contentType="application/json",
    )
    return json.loads(response["body"].read())["embedding"]  # type: ignore[no-any-return]
