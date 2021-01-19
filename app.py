import os
import re
from pathlib import Path
from string import punctuation
from typing import List
import pandas as pd

import joblib
import streamlit as st
from sentence_transformers import SentenceTransformer

from regexes import removals, substitutions
from download import download_link

os.environ["TOKENIZERS_PARALLELISM"] = "true"

ALL_PUNCTUATION = punctuation + "‘’"


@st.cache
def cleaner(text):
    if pd.isnull(text):
        return ""
    # Remove Commas from Numbers
    text = re.sub(r"(\d+?),(\d+?)", r"\1\2", text)
    # Do all substitutions (Case insensitive on raw text)
    for substitution in substitutions:
        text = re.sub(substitution.regex, substitution.replacement, text)
    # Remove any terms we don't want
    for removal in removals:
        text = re.sub(removal.regex, " ", text)
    # Then remove remaining punctuation
    for punct in ALL_PUNCTUATION:
        text = text.replace(punct, " ")
    text = " ".join(text.split())  # removes extra spaces: "  " → " "
    text = text.lower()
    return text


@st.cache(allow_output_mutation=True)
def load_embedder():
    embedder = SentenceTransformer("distilroberta-base-paraphrase-v1")
    return embedder


st.markdown(Path("intro.md").read_text())
embedder = load_embedder()

MODEL = "distilroberta-base-paraphrase-v1.lr"
model = joblib.load(MODEL)


@st.cache
def predict(text: str):
    clean = cleaner(text)
    embed = embedder.encode([clean], show_progress_bar=False)
    preds = model.predict(embed)
    return preds


@st.cache
def predict_bulk(texts: List[str]):
    print(texts)
    cleaned = [cleaner(text) for text in texts]
    embed = embedder.encode(cleaned, show_progress_bar=False)
    preds = model.predict(embed)
    return preds


st.markdown("## ✏️ Single Coder Demo")
input_text = st.text_input(
    "Input Offense",
    value="FRAUDULENT USE OF A CREDIT CARD OR DEBT CARD >=$25,000",
)

predictions = predict(input_text)

labels = ["Broad Category", "BJS Category", "BJS Description"]
predictions_labeled = dict(zip(labels, predictions[0]))
st.write(predictions_labeled)

st.markdown("## 📑 Bulk Coder")
uploaded_file = st.file_uploader("Bulk Upload", type=["xlsx", "csv"])

if uploaded_file is not None:
    if uploaded_file.name.endswith("xlsx"):
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    elif uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)

    st.write("Select Column of Text")
    selected_column = st.selectbox("Select Column of Texts", options=list(df.columns))

    input_texts = df[selected_column].tolist()
    bulk_preds = predict_bulk(input_texts)
    for i, column in enumerate(labels):
        df[column] = bulk_preds[:, i]

    st.write("Sample")
    st.dataframe(df.head(100))

    if st.button("Download Dataframe as CSV"):
        tmp_download_link = download_link(
            df,
            f"{uploaded_file.name}-ncrp-predictions.csv",
            "Click here to download your data!",
        )
        st.markdown(tmp_download_link, unsafe_allow_html=True)
