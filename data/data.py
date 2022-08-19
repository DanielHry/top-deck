import os
import pandas as pd
import streamlit as st

DIR = os.path.dirname(__file__)

@st.cache
def load_data():
    return pd.read_csv(DIR + "/data_decs.csv")