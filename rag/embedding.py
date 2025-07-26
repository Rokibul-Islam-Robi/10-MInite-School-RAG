import os
import requests # Using requests for direct API calls as per your setup
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# Use the correct embedding endpoint URL
GEMINI_EMBEDDING_URL = 'https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent'

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

def get_embedding(text: str, task_type: str):
    """
    Generates an embedding for the given text using the Gemini embedding model
    via direct REST API call.
    Requires a task_type ("retrieval_document" or "retrieval_query").
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected text input to be a string, got {type(text)}")
    if not text.strip():
        # Returning an empty list or raising an error for empty text might be better depending on downstream
        raise ValueError("Cannot get embedding for empty or whitespace-only text.")

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "model": "models/embedding-001",
        "content": {"parts": [{"text": text}]},
        "task_type": task_type, # CRITICAL FIX: Add the required task_type
        # "title": "Document chunk" if task_type == "retrieval_document" else "Query" # Optional, can be added for context
    }

    try:
        response = requests.post(GEMINI_EMBEDDING_URL, headers=headers, params=params, json=data)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        json_response = response.json()

        # Check if the 'embedding' key exists in the response
        if 'embedding' in json_response and 'values' in json_response['embedding']:
            return json_response['embedding']['values']
        else:
            raise ValueError(
                f"Unexpected response structure from Embedding API. "
                f"'embedding' or 'values' key missing. Full response: {json_response}"
            )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Gemini Embedding API request failed: {e}. Response text: {response.text if 'response' in locals() else 'No response content'}")
    except Exception as e:
        raise Exception(f"Gemini Embedding API error: {str(e)}")

def embed_chunks(chunks):
    """
    Generates embeddings for a list of text chunks using 'retrieval_document' task_type.
    """
    embedded = []
    print(f"DEBUG: Starting embedding of {len(chunks)} chunks.")
    for i, chunk in enumerate(chunks):
        if i % 10 == 0:
            print(f"DEBUG: Embedding chunk {i+1}/{len(chunks)}...")
        try:
            # Pass task_type="retrieval_document" for document chunks
            emb = get_embedding(chunk, task_type="retrieval_document")
            if emb is not None:
                embedded.append((i, chunk, emb))
        except Exception as e:
            print(f"WARNING: Skipping chunk {i} due to embedding error: {e}")
            continue
    print(f"DEBUG: Finished embedding chunks. Successfully embedded {len(embedded)} chunks.")
    return embedded

def embed_query(query_text):
    """
    Embeds a single query text using 'retrieval_query' task_type.
    Returns a tuple (0, query_text, embedding_vector) to match db.py's expectation.
    """
    print(f"DEBUG: Embedding query text (first 50 chars): '{query_text[:50]}...'")
    # Pass task_type="retrieval_query" for the query text
    query_emb = get_embedding(query_text, task_type="retrieval_query")
    if query_emb is None:
        raise Exception("Failed to embed query text, embedding was None.")
    print(f"DEBUG: Query embedding length: {len(query_emb)}")
    return (0, query_text, query_emb)