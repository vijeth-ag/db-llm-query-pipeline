import requests
from openai import OpenAI
import json

def get_similar_docs(question):
    response = requests.get("http://db-service:5123/get?query="+question)
    if response.status_code == 200:
        return response.text
    else:
        return []

def get_results(question, context):
    print("getting results..........")
    url = "http://host.docker.internal:1234/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": "LM Studio Community/Meta-Llama-3-8B-Instruct-GGUF",
        "messages": [
            { "role": "system", "content": "Given the following context, perform query and reply with results: " + context },
            { "role": "user", "content": question }
        ],
        "temperature": 0.5,
        "max_tokens": -1,
        "stream": True
    }

    response = requests.post(url, headers=headers, json=data)

    full_response_content = ""

    # Process the response chunks
    for chunk in response.iter_lines():
        if chunk:
            # Decode and remove the 'data: ' prefix if present
            chunk_str = chunk.decode('utf-8')
            if chunk_str.startswith("data: "):
                chunk_str = chunk_str[6:]

            # Parse the chunk as JSON
            try:
                chunk_data = json.loads(chunk_str)
            except json.JSONDecodeError:
                continue  # Skip any invalid JSON

            # Check if 'choices' exist and merge the content
            if 'choices' in chunk_data:
                for choice in chunk_data['choices']:
                    delta = choice.get('delta', {})
                    content = delta.get('content', '')
                    full_response_content += content

    print("full_response_content",full_response_content)
    return full_response_content



