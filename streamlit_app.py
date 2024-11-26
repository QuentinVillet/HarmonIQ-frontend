import streamlit as st
import requests

response = requests.get("http://localhost:8000/")
data = response.json()

st.write(data['greeting'])

st.write(data['greeting2'])

#THese are examples and just used to set up the streamlit with fastapi for us to create the front end
