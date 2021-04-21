import os
from typing import Any, Dict, List

import streamlit as st
from transformers import (
    RobertaForSequenceClassification,
    RobertaTokenizer,
    TextClassificationPipeline,
)

from cleaning_utils import cleaner


@st.cache
def cleaner_cache(text):
    return cleaner(text)


os.environ["TOKENIZERS_PARALLELISM"] = "true"


def load_model():
    pipeline = TextClassificationPipeline(
        tokenizer=RobertaTokenizer.from_pretrained(
            "rti-international/distilroberta-ncrp-classification"
        ),
        model=RobertaForSequenceClassification.from_pretrained(
            "rti-international/distilroberta-ncrp-classification"
        ),
        return_all_scores=True,
    )
    return pipeline


pipeline = load_model()


def predict(text: str, sort=True) -> List[List[Dict[str, Any]]]:
    """Generate a single prediction on an input text

    Args:
        text (str): The input text to generate a prediction for (post-clean)
        sort (bool, optional): Whether to sort the predicted labels by score. Defaults to True.

    Returns:
        List[List[Dict[str, Any]]]: A list with a single element containing predicted label scores.
    """
    clean = cleaner_cache(text)
    preds = pipeline([clean])
    if sort:
        sorted_preds = [
            sorted(p, key=lambda d: d["score"], reverse=True) for p in preds
        ]
        return sorted_preds
    else:
        return preds


def predict_bulk(texts: List[str]) -> List[List[Dict[str, Any]]]:
    """Generate predictions on a list of strings.

    Args:
        texts (List[str]): Input texts to generate predictions (post-cleaning)

    Returns:
        List[List[Dict[str, Any]]]: Predicted label scores for each input text
    """
    cleaned = [cleaner_cache(text) for text in texts]
    preds = pipeline(cleaned)
    return preds


def _max_pred(prediction_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Utility function to find the maximum predicted label
    for a single prediction

    Args:
        prediction_scores (List[Dict[str, Any]]): A list of predictions with keys
            'label' and 'score'

    Returns:
        Dict[str, Any]: The 'label' and 'score' dict with the highest score value
    """
    return max(prediction_scores, key=lambda d: d["score"])


def max_pred_bulk(preds: List[List[Dict[str, Any]]]) -> List[str]:
    """Generates a "column" of label predictions by finding the max
    prediction score per element

    Args:
        preds (List[List[Dict[str, Any]]]): A list of predictions

    Returns:
        List[str]: A list of labels with the max predicted score
    """
    return [_max_pred(pred)["label"] for pred in preds]
