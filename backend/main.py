from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/text-to-image"

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
def generate_image(data: Prompt):
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "image/png"
        },
        files={"none": (None, data.prompt)}
    )

    if response.status_code != 200:
        return {"error": "Generation failed"}

    return {
        "image_base64": response.content.encode("base64")
    }
