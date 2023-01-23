import os

import pandas as pd
import streamlit as st
from pandas import DataFrame
import rubus
from rubus.manage_data import dir_all

st.set_page_config(page_title="Management", page_icon="🧊", layout="wide", initial_sidebar_state="auto")

############################
#
# Track Log Management
#
############################
st.subheader("Track Log Management")
with st.container():
    ph_dataframe = st.empty()
    ph_multiselect = st.empty()

    df: DataFrame = dir_all(rubus.TRACKLOGS_DIR)
    df = df[df["type"] == "file"]
    ph_dataframe.dataframe(df[["name", "size", "last_updated"]])
    options = df.index.values.tolist()
    selections = ph_multiselect.multiselect("Remove the selected track logs", options=options, format_func=lambda x: df.iloc[x]["name"])
    if st.button("Delete"):
        df_selected= df.iloc[selections]
        df_unselected = df.iloc[ [i for i in set(options) if i not in selections]]
        df_selected.apply(lambda x: os.remove(x["full_name"]), axis=1)

        ph_dataframe.dataframe(df_unselected[["name", "size", "last_updated"]])
        options = df_unselected.index.values.tolist()
        ph_multiselect.multiselect("Remove the selected track logs", options=options, format_func=lambda x: df.iloc[x]["name"])



############################
#
# Resource Management
#
############################
# st.subheader("Resource Management")
# with st.container():
#     st.write("TBC")
