from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from src import logger
from config import GRAMMAR_MODEL_NAME

_model = None
_tokenizer = None


def get_grammar_model():
    global _model, _tokenizer

    if _model is None:
        logger.info(f"Loading grammar model: {GRAMMAR_MODEL_NAME}")
        _tokenizer = T5Tokenizer.from_pretrained(GRAMMAR_MODEL_NAME)
        _model = T5ForConditionalGeneration.from_pretrained(GRAMMAR_MODEL_NAME)
        logger.info("Grammar model loaded successfully")

    return _model, _tokenizer


class GrammarChecker:

    @staticmethod
    def correct_text(text: str):

        model, tokenizer = get_grammar_model()

        input_text = "fix grammar: " + text

        input_ids = tokenizer.encode(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )

        outputs = model.generate(
            input_ids,
            max_length=512,
            num_beams=4,
            early_stopping=True
        )

        corrected_text = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return corrected_text
