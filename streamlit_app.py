import streamlit as st
import requests

response = requests.get("http://localhost:8000/")
data = response.json()

st.write(data['greeting'])

st.write(data['greeting2'])

#THese are examples and just used to set up the streamlit with fastapi for us to create the front end

client_secret = st.secrets['client_secret']
client_id = st
client_secret = '7deaab2f08154a97905868d89919fc55'
redirect_uri = 'https://localhost:8888/callback/'
scope = "playlist-modify-private user-library-read playlist-read-private"

if st.button('log into your spotify account'):


    st.write('')



params={'playlistid':lstplaylistids}

response=requests.get(f'http://localhost8000/endpointinyourapi,{params}=params')

if response ==200:
    response.json()
