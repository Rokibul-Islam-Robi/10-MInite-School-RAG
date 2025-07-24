import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_EMBEDDING_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent'


def get_embedding(text):
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "model": "models/gemini-embedding-001",
        "content": {"parts": [{"text": text}]},
        "embedding_config": {"output_dimensionality": 1536}
    }
    response = requests.post(GEMINI_EMBEDDING_URL, headers=headers, params=params, json=data)
    if response.status_code == 200:
        return response.json()['embedding']['values']
    else:
        raise Exception(f"Gemini Embedding API error: {response.text}")


def embed_chunks(chunks):
    embedded = []
    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        embedded.append((i, chunk, emb))
    return embedded 