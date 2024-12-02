import streamlit as st
import requests
import webbrowser

# Flask API base URL
API_BASE_URL = "http://127.0.0.1:5000"

# Step 1: Login
st.title("Spotify Streamlit App")

if st.button("Login to Spotify"):
    response = requests.get(f"{API_BASE_URL}/login")
    if response.status_code == 200:
        auth_url = response.json().get("auth_url")
        if auth_url:
            webbrowser.open(auth_url)
            st.success("Opened Spotify login page in your browser.")
    else:
        st.error("Failed to connect to Spotify login.")
