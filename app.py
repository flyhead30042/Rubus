import os.path
from io import BytesIO

import streamlit as st

from rubus import IMAGES_DIR

st.set_page_config(
    page_title="streamlit-folium documentation",
    page_icon=":world_map:️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write("# Welcome to Rubus! 👋")

st.markdown(
    """
    This is Rubus project 
    """
)

with st.container():
    img = BytesIO()
    with open(os.path.join(IMAGES_DIR, "1.png"), "rb") as f:
        img.write(f.read())

    st.image(img, caption='Praça Ferreira do Amaral, Macau', width=450)

with st.sidebar:
    build = os.environ.get("BUILD", "Unknown")
    st.write(f"build # = {build}")



