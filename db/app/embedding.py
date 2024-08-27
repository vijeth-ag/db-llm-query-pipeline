import requests
import os
import time
from openai import OpenAI

hf_token = os.getenv("HF_TOKEN")

# model_id = "sentence-transformers/all-MiniLM-L6-v2"

# api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
client = OpenAI(base_url="http://host.docker.internal:1234/v1", api_key="lm-studio")
headers = {"Authorization": f"Bearer {hf_token}"}


def encode(final_sentence, model="nomic-ai/nomic-embed-text-v1.5-GGUF"):
   final_sentence = final_sentence.replace("\n", " ")
   response = client.embeddings.create(input = [final_sentence], model=model).data[0].embedding
   return response

    # retries = 5
    # for i in range(retries):
    #     response = requests.post(api_url, headers=headers, json={"inputs": final_sentence, "options":{"wait_for_model":True}})
    #     print("response.status_code",response.status_code)
    #     if response.status_code == 429:
    #         wait_time = 2 ** i  # Exponential backoff
    #         print(f"Rate limited. Retrying in {wait_time} seconds...")
    #         time.sleep(wait_time)
    #     else:
    #         return response.json()
    # return None


    