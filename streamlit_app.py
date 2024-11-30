import streamlit as st
import requests

# response = requests.get("http://localhost:8501")
# data = response.json()

# st.write(data['greeting'])

# st.write(data['greeting2'])

st.write('placeholder')
#THese are examples and just used to set up the streamlit with fastapi for us to create the front end

if st.button('log into your spotify account'):


    st.write('')



params={'playlistid':'lstplaylistids'}

response=requests.get(f'http://localhost8000/endpointinyourapi,{params}=params')

if response ==200:
    response.json()
