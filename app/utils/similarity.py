from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def rank_by_cosine_similarity(idea_embedding, doc_embeddings, docs):
    sims = cosine_similarity([idea_embedding], doc_embeddings)[0]
    ranked = sorted(zip(sims, docs), key=lambda x: x[0], reverse=True)
    return [doc for _, doc in ranked]
