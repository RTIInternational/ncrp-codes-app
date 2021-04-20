import os
from functools import partial
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import streamlit as st
from transformers import (
    RobertaForSequenceClassification,
    RobertaTokenizer,
    TextClassificationPipeline,
)

from cleaning_utils import cleaner
from download import download_link

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


@st.cache
def cleaner_cache(text):
    return cleaner(text)


def predict(text: str, sort=True):
    clean = cleaner_cache(text)
    preds = pipeline([clean])
    if sort:
        sorted_preds = [
            sorted(p, key=lambda d: d["score"], reverse=True) for p in preds
        ]
        return sorted_preds
    else:
        return preds


def predict_bulk(texts: List[str]):
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
    prediction score per row

    Args:
        preds (List[List[Dict[str, Any]]]): A list of predictions

    Returns:
        List[str]: A list of labels with the max predicted score
    """
    return [_max_pred(pred)["label"] for pred in preds]


st.markdown(Path("readme.md").read_text())

st.markdown("---")
st.markdown("## ✏️ Single Coder Demo")
input_text = st.text_input(
    "Input Offense",
    value="FRAUDULENT USE OF A CREDIT CARD OR DEBT CARD >= $25,000",
)

predictions = predict(input_text)

st.markdown("Predictions")
labels = ["Charge Category"]
predictions_labeled = dict(zip(labels, predictions))
st.write(predictions_labeled)

st.markdown("---")
st.markdown("## 📑 Bulk Coder")
st.markdown("1️⃣ **Upload File**")
uploaded_file = st.file_uploader("Bulk Upload", type=["xlsx", "csv"])

file_readers = {"csv": pd.read_csv, "xlsx": partial(pd.read_excel, engine="openpyxl")}

if uploaded_file is not None:
    for filetype, reader in file_readers.items():
        if uploaded_file.name.endswith(filetype):
            df = reader(uploaded_file)

    st.write("2️⃣ **Select Column of Offense Descriptions**")
    string_columns = list(df.select_dtypes("object").columns)
    longest_column = max(
        [(df[c].str.len().mean(), c) for c in string_columns], key=lambda x: x[0]
    )[1]

    selected_column = st.selectbox(
        "Select Column",
        options=list(string_columns),
        index=string_columns.index(longest_column),
    )
    st.write("Uploaded Data Sample")
    st.dataframe(df.head(20))
    st.write(f"3️⃣ **Predict Using Column: `{selected_column}`**")

    if st.button(f"Compute Predictions"):
        input_texts = df[selected_column].tolist()
        with st.spinner("Making Predictions"):
            bulk_preds = predict_bulk(input_texts)
        pred_copy_df = df.copy()
        pred_copy_df["charge_category_pred"] = max_pred_bulk(bulk_preds)

        # TODO: Add all scores

        st.write("Sample Output")
        st.dataframe(pred_copy_df.head(100))

        tmp_download_link = download_link(
            pred_copy_df,
            f"{uploaded_file.name}-ncrp-predictions.csv",
            "⬇️ Download as CSV",
        )
        st.markdown(tmp_download_link, unsafe_allow_html=True)
