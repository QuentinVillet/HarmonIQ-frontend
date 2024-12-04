import streamlit as st

import numpy as np
import pandas as pd


st.markdown("""# Welcome to HarmonIQ
## Find your next best song""")


#we need to connect to Spotify

st.text_input("Insert your spotify user_name", key="name")

# You can access the value at any point with:
st.session_state.name


st.text_input("Insert your password-<need hashed>", key="password")

# You can access the value at any point with:
st.session_state.password






"when authenticated - a validation message "



st.markdown("""
            .
            ## How it works""")

df = pd.DataFrame({
    'Stage 1': ['Analyse User Account'],
    'Stage 2': ['Provide Summary'],
    'Stage 3': ['Make Suggestions']
})

#Showing process stages of the app

st.dataframe(data=df, width=900)
