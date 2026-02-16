from sentence_transformers import SentenceTransformer
from config import MODEL_NAME
from src import logger

_model = None


def get_model():
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
        logger.info("Model loaded successfully")
    return _model


def encode_text(text: str):
    model = get_model()
    return model.encode(text)
