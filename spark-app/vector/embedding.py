import requests
import os

hf_token = os.getenv("HF_TOKEN")


model_id = "sentence-transformers/all-MiniLM-L6-v2"

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}


def encode(final_sentence):
    response = requests.post(api_url, headers=headers, json={"inputs": final_sentence, "options":{"wait_for_model":True}})
    return response.json()