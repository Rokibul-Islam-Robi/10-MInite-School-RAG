from rag.db import search_similar_chunks
# No need to import embed_query here, as db.py will handle embedding the query

def retrieve_relevant_chunks(query_text, top_k=4):
    """
    Retrieves the top_k most relevant chunks for a given query text from the database.
    The query text is embedded within search_similar_chunks.
    """
    print(f"DEBUG: Retrieving relevant chunks for query: '{query_text}'")
    # CRITICAL FIX: Pass the original query_text directly to search_similar_chunks.
    # search_similar_chunks in db.py will now handle embedding the query internally.
    results = search_similar_chunks(query_text, top_k=top_k)
    return results