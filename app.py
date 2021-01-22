import os
import re
from pathlib import Path
from string import punctuation
from typing import List
import pandas as pd

import joblib
import streamlit as st
from sentence_transformers import SentenceTransformer

from cleaning_utils import cleaner
from download import download_link
from functools import partial

os.environ["TOKENIZERS_PARALLELISM"] = "true"

ALL_PUNCTUATION = punctuation + "‘’"


@st.cache
def cleaner_cache(text):
    return cleaner(text)


@st.cache(allow_output_mutation=True)
def load_embedder():
    embedder = SentenceTransformer("distilroberta-base-paraphrase-v1")
    return embedder


@st.cache
def predict(text: str):
    clean = cleaner_cache(text)
    embed = embedder.encode([clean], show_progress_bar=False)
    preds = model.predict(embed)
    return preds


@st.cache
def predict_bulk(texts: List[str]):
    cleaned = [cleaner_cache(text) for text in texts]
    embed = embedder.encode(cleaned, show_progress_bar=False)
    preds = model.predict(embed)
    return preds


MODEL = "distilroberta-base-paraphrase-v1.20210122-091032.lr"
model = joblib.load(MODEL)

st.markdown(Path("readme.md").read_text())
embedder = load_embedder()

st.markdown("---")
st.markdown("## ✏️ Single Coder Demo")
input_text = st.text_input(
    "Input Offense",
    value="FRAUDULENT USE OF A CREDIT CARD OR DEBT CARD >= $25,000",
)

predictions = predict(input_text)

st.markdown("Predictions")
labels = ["Broad Category", "BJS Category", "BJS Description"]
predictions_labeled = dict(zip(labels, predictions[0]))
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
        for i, column in enumerate(labels):
            pred_copy_df[column] = bulk_preds[:, i]

        st.write("Sample Output")
        st.dataframe(pred_copy_df.head(100))

        tmp_download_link = download_link(
            pred_copy_df,
            f"{uploaded_file.name}-ncrp-predictions.csv",
            "⬇️ Download as CSV",
        )
        st.markdown(tmp_download_link, unsafe_allow_html=True)
