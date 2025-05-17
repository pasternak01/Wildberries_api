import streamlit as st
import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [55.75, 37.61],
    columns=['lat', 'lon'])

st.map(map_data)
st.write("Hello Woooorld!")