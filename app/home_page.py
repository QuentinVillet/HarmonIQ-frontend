import streamlit as st
import os
import spotipy
from spotipy import Spotify, SpotifyException
from urllib.parse import urlencode
import requests



# Spotify app credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "https://harmoniq-frontend-9hxq9xgg7clppw9nwuzy8p.streamlit.app"
SCOPE = "playlist-modify-private user-library-read playlist-read-private"

# Spotify URLs
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


# Define available pages
PAGES = {
    "Dashboard": "home",
    "New playlist": "playlist",  # Optional additional pages
}

# Page selection
st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to", list(PAGES.keys()))


def home_page():
    st.title(f"""Welcome to HarmonIQ.""")
    st.query_params.update(page='home')

    # Log in
    if 'access_token' not in st.session_state:
        try:
            st.session_state['access_token'] = None
            params = {
                "client_id": CLIENT_ID,
                "response_type": "code",
                "redirect_uri": REDIRECT_URI,
                "scope": SCOPE,
            }
            auth_url = f"{AUTH_URL}?{urlencode(params)}"

            # st.write("To start, authenticate with Spotify.")
            st.markdown(f"[Login with Spotify]({auth_url})")

            # Use st.query_params to fetch the code
            st.query_params.update(page="home")
            query_params = st.query_params
            code = query_params.get("code")
            if code:
                code = code

                # Exchange the code for access token
                token_data = {
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                }
                response = requests.post(TOKEN_URL, data=token_data)

                if response.status_code == 200:
                    token_info = response.json()
                    st.session_state.logged_in = True
                    st.session_state["access_token"] = token_info["access_token"]
                    st.session_state["refresh_token"] = token_info.get("refresh_token")
                    st.success("Authentication successful!")
                    st.query_params.update(page="home")

        except SpotifyException as e:
            # Log the error for debugging
            st.error("An error occurred while fetching user data. Please try again.")
            print(f"SpotifyException: {e}")


    # Dashboard
    sp = spotipy.Spotify(auth=st.session_state['access_token'])
    user = sp.current_user()
    st.session_state.user_name = user['display_name']
    st.title(f"""Good to see you {st.session_state.user_name} !""")
    st.write("Let's take a look at your profile...")

    st.query_params.update(page="playlist")
    st.title("Welcome to your playlist generator")

    if st.button("show my playlists"):
        sp = spotipy.Spotify(auth=st.session_state['access_token'])
        results = sp.current_user_playlists(limit=50)

        # playlists = [{'name':item['name'], 'id':item['id']} for item in results['items']]
        # # st.write(playlists)
        # for playlist in playlists:
        #     st.button(f'{playlist["name"]} ({playlist["id"]})')

        playlists = results.json().get('items', [])
        for playlist in playlists:
            if st.button(f"🎵 {playlist['name']} ({playlist['tracks']['total']} tracks)"):
                st.write('tracks')


if __name__ == "__main__":
    home_page()




# Log out
if st.button("Log out"):
    st.session_state.clear()
    st.success("Logged out successfully! Redirecting to the login page...")
    st.query_params.update(page="home")
    st.rerun()
