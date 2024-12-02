import streamlit as st

import numpy as np
import pandas as pd


st.markdown("""# HarmonIQ-App
## 1# Spotify Account Analysis""")

st.write("User Spotify Account Summary")
# Provide top level stats on user account - #playlists, #songs, #age, #favourites





df2 = pd.DataFrame({
    'Total playlists': ['data #1'],
    'Total songs': ['data #2'],
    'Account age': ['data #3'],
    'Activity': ['data #4']
})

df2



st.markdown("""## 2# User Playlist Selection""")
# <put likes folder at top>


st.write("Your playlists ")


df3 = pd.DataFrame({
    'Playlist name': ['playlist 1', 'playlist 2'],
    'Details': ['playlist 1 details', 'playlist 2 details']
})

st.dataframe(data=df3, width=900)



option = st.selectbox(
    'Select playlist to run',
     df3['Playlist name'])

'You selected: ', option

#when playlist selected- run loading widget?

# st.markdown("***")

st.markdown("""
            .
            ## 3# Song Recommendations """)



st.write("Based off the H-Model > serve up 3x songs ")

# # Provide top level stats on user account - #playlists, #songs, #age, #favourites

Accept_recos= "Artist, song, genre of songs + URL to spotify ac to play "
Accept_recos
