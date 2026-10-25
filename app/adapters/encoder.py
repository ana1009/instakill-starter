from sentence_transformers import SentenceTransformer

class TextEncoder:
    """
    Adapter for the pretrained embedding model.
    Keeps ML dependencies isolated from HTTP and application logic.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, normalize: bool = True):
        return self.model.encode(texts, normalize_embeddings=normalize)

# Global instance to be loaded once
encoder = TextEncoder()