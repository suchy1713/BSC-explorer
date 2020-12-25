import streamlit as st
import pandas as pd

def format_datetime(dt):
    dt = pd.to_datetime(str(dt))
    return dt.strftime('%Y-%m-%d')

def set_style():
    st.markdown("""
<style>
body {
    color: #cdcdcd;
    background-color: #131313;
}
.stSelectbox {
    color: #cdcdcd
}
.stButton>button {
    color: #4F8BF9;
    border-radius: 50%;
    height: 3em;
    width: 3em;
}

.stTextInput>div>div>input {
    color: #4F8BF9;
}
</style>
    """, unsafe_allow_html=True)