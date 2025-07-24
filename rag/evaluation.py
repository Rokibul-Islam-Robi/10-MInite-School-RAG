from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# For automatic evaluation

def evaluate_groundedness(answer_embedding, context_embeddings):
    # Returns the max cosine similarity between answer and any context chunk
    sims = cosine_similarity([answer_embedding], context_embeddings)
    return float(np.max(sims))

# For human-labeled evaluation, compare system answer to expected answer

def evaluate_relevance(retrieved_chunks, expected_chunks):
    retrieved_ids = set([c[0] for c in retrieved_chunks])
    expected_ids = set(expected_chunks)
    return len(retrieved_ids & expected_ids) / max(1, len(expected_ids)) 