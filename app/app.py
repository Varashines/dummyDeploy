import boto3
from fastapi import FastAPI
import os

app = FastAPI()
region = os.getenv("AWS_REGION", "us-east-1")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI with Bedrock and DynamoDB!"}

@app.get("/generate")
def generate_text(prompt: str = "Hello Bedrock"):
    client = boto3.client("bedrock-runtime", region_name=region)
    # Using titanium-g1-express as an example
    try:
        response = client.invoke_model(
            modelId="amazon.titan-text-express-v1",
            body=f'{{"inputText": "{prompt}", "textGenerationConfig": {{"maxTokenCount": 50, "temperature": 0.7}}}}'
        )
        return {"response": response["body"].read().decode()}
    except Exception as e:
        return {"error": str(e)}

@app.get("/db-test")
def test_db():
    dynamodb = boto3.resource("dynamodb", region_name=region)
    # This is just to test connectivity
    try:
        tables = list(dynamodb.tables.all())
        return {"tables": [t.name for t in tables]}
    except Exception as e:
        return {"error": str(e)}
