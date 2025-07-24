# Uses Gemini embeddings for retrieval
from .embedding import get_embedding
from .db import search_similar_chunks


def retrieve_relevant_chunks(query, top_k=4):
    query_emb = get_embedding(query)
    results = search_similar_chunks(query_emb, top_k=top_k)
    # results: [(chunk_id, text, distance), ...]
    return results 