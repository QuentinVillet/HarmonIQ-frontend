import streamlit as st
import app.login as login
import app.home_page as home_page
import app.playlist_page as playlist_page



query_params = st.query_params()
page = query_params.get("page", ["home"])[0]

# Dynamically render the page
if page == "home":
    home_page.home_page()
elif page == "playlist":
    playlist_page.get_playlists()
else:
    st.error("Page not found!")


# Define available pages
PAGES = {
    "Home": "home",
    "New playlist": "playlist",  # Optional additional pages
}

# Page selection
st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to", list(PAGES.keys()))
