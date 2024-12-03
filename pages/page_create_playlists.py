import streamlit as st
import requests
import webbrowser

# Flask API base URL
API_BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "access_token" not in st.session_state:
    st.session_state.access_token = None


def show_login_page():

    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    st.title("Welcome ot HarmonIQ")
    if st.button("Log in my Spotify"):
        response = session.get(f"{API_BASE_URL}/login")
        if response.status_code == 200:
            auth_url = response.json().get("auth_url")
            if auth_url:
                webbrowser.open(auth_url)
                st.success("Opened Spotify login page in your browser.")
        else:
            st.error("Failed to connect to Spotify login.")

    # Handle Redirect from Spotify
    query_params = st.query_params
    if "success" in query_params:
        if query_params["success"] == "true" and "token" in query_params:
            st.success("Successfully logged in to Spotify!")
            st.session_state.access_token = query_params["token"]
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error(f"Spotify login failed. Please try again.")




def show_main_page():

    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(f"{API_BASE_URL}/user", headers=headers)
    st.session_state.user_name = response.json()['display_name']
    st.title(f"""Nice to meet you {st.session_state.user_name}""")


    # Cached function to fetch playlists
    @st.cache_data
    def fetch_playlists(access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_BASE_URL}/playlists", headers=headers)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            st.error("Failed to fetch playlists.")
            return []

    # Store selected playlist details
    if "selected_playlists" not in st.session_state:
        st.session_state.selected_playlists = []

    if st.session_state.access_token:
        playlists = fetch_playlists(st.session_state.access_token)

        # Display playlists and allow the user to select
        if playlists:
            st.write("Playlists:")
            for playlist in playlists:
                playlist_id = playlist["id"]
                playlist_name = playlist["name"]
                track_count = playlist["tracks"]["total"]

                # Add button for each playlist
                if st.button(f"🎵 {playlist_name} ({track_count} tracks)", key=playlist_id):
                    # Cache the id and name of the playlist
                    st.session_state.selected_playlists.append({"id": playlist_id, "name": playlist_name})
                    st.success(f"Added playlist '{playlist_name}' to the cache!")
        else:
            st.write("No playlists found.")

    # Display cached playlists
    if st.session_state.selected_playlists:
        st.write("Cached Playlists:")
        for saved_playlist in st.session_state.selected_playlists:
            st.write(f"🎵 {saved_playlist['name']}")




# Log out
if st.button("log out"):
    st.session_state.clear()
    st.write(st.session_state)
    show_login_page()


# debug session
if st.checkbox("debugging"):
    st.write(st.session_state)


if st.session_state.logged_in == True and st.session_state.access_token:
    show_main_page()
else:
    show_login_page()
