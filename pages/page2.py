import streamlit as st

import numpy as np
import pandas as pd


st.markdown("""# HarmonIQ-App
## 1# Spotify Account Analysis""")

st.write("User Spotify Account Summary")

df2 = pd.DataFrame({
    'Total playlists': ['data #1'],
    'Total songs': ['data #2'],
    'account age': ['data #3'],
    'fourth column': ['data #4']
})
df2

# Provide top level stats on user account - #playlists, #songs, #age, #favourites


st.markdown("""## 2# User Playlist Selection""")

st.write("Select your playlist <put likes at top> ")


df3 = pd.DataFrame({
    'Playlist name': ['data #1'],
    'Details': ['data #2']
})

st.dataframe(data=df3, width=900, height=200,)




st.markdown("""## 3# Song Recommendations""")

st.write("Based off the H-Model <> ")

# # Provide top level stats on user account - #playlists, #songs, #age, #favourites


# line_count = st.slider('Select a line count', 1, 10, 3)

# st.write("Your playlists")


# # and used to select the displayed lines
# head_df = df.head(line_count)



# head_df
