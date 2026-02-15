import streamlit as st
import pandas as pd
from io import StringIO

st.title("Report Generator")
st.write("If you can see this, Streamlit is rendering.")

uploaded_file = st.file_uploader("Please upload Match CSV")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
