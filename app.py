import os
from functools import partial
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import streamlit as st
from more_itertools import ichunked
from stqdm import stqdm

from model_utils import predict, predict_bulk, max_pred_bulk
from download import download_link

PRED_BATCH_SIZE = 500

st.set_page_config(
    page_title="NCRP Offense Code Classifier", initial_sidebar_state="collapsed"
)

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
st.dataframe(pd.DataFrame(predictions[0]))

st.markdown("---")
st.markdown("## 📑 Bulk Coder")
st.warning(
    "⚠️ *Note:* Your input data will be deduplicated"
    " on the selected column to reduce computation requirements."
)
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
    df_unique = df.drop_duplicates(subset=[selected_column])
    st.markdown(
        f"Uploaded Data Sample `(Deduplicated. N Rows = {len(df_unique)}, Original N = {len(df)})`"
    )
    st.dataframe(df_unique.head(20))
    st.write(f"3️⃣ **Predict Using Column: `{selected_column}`**")

    if st.button(f"Compute Predictions"):
        input_texts = (value for _, value in df_unique[selected_column].items())

        n_batches = (len(df_unique) // PRED_BATCH_SIZE) + 1

        bulk_preds = []
        for batch in stqdm(
            ichunked(input_texts, PRED_BATCH_SIZE),
            total=n_batches,
            desc="Bulk Predict Progress",
        ):
            batch_preds = predict_bulk(batch)
            bulk_preds.extend(batch_preds)

        pred_copy_df = df_unique.copy()
        pred_copy_df["charge_category_pred"] = max_pred_bulk(bulk_preds)

        # # TODO: Add all scores

        st.write("**Sample Output**")
        st.dataframe(pred_copy_df.head(100))

        tmp_download_link = download_link(
            pred_copy_df,
            f"{uploaded_file.name}-ncrp-predictions.csv",
            "⬇️ Download as CSV",
        )
        st.markdown(tmp_download_link, unsafe_allow_html=True)
