# VectorDB operations placeholder 
from chromadb.utils import embedding_functions
import chromadb

# Assume chroma already initialized
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("validated_ideas")

def store_vector(embedding: list, metadata: dict):
    collection.add(
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[metadata.get("verdict", "unknown") + "_" + str(hash(str(metadata)))]
    )
