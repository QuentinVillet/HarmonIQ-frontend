# import streamlit as st
# import requests
# import webbrowser


# if "access_token" not in st.session_state:
#     st.session_state.access_token = None

# # Flask API base URL
# API_BASE_URL = "http://127.0.0.1:5000"


# st.markdown("""# Welcome to HarmonIQ""")

# # Login
# st.title("Spotify Streamlit App")

# if st.button("Login to Spotify"):
#     response = requests.get(f"{API_BASE_URL}/login")
#     if response.status_code == 200:
#         auth_url = response.json().get("auth_url")
#         if auth_url:
#             webbrowser.open(auth_url)
#             st.success("Opened Spotify login page in your browser.")
#     else:
#         st.error("Failed to connect to Spotify login.")

# # Handle Redirect from Spotify
# query_params = st.query_params
# if "success" in query_params:
#     if query_params["success"] == "true":
#         st.success("Successfully logged in to Spotify!")
#         st.session_state.access_token = query_params["token"]
#         st.write(st.session_state)
#     else:
#         st.error(f"Spotify login failed. Please try again.")


# # Log out
# if st.button("log out"):
#     response = requests.get(f"{API_BASE_URL}/logout")
#     if response.status_code == 200:
#         st.success('succesfully logged out')
#     else:
#         st.error(f'error {response.status_code}')



# # Fetch Playlists
# if st.button("Get Playlists"):
#     headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
#     response = requests.get(f"{API_BASE_URL}/playlists", headers=headers)

#     if response.status_code == 200:
#         playlists = response.json().get('items', [])
#         for playlist in playlists:
#             if st.button(f"🎵 {playlist['name']} ({playlist['tracks']['total']} tracks)"):
#                 st.write(f"{playlist['tracks']}")
#                 # for track in tracks:
#                 #         st.write(f"🎵 {track['name']} ({track['tracks']['total']} tracks)")

#     elif response.status_code == 401:
#         st.error("You are not logged in. Please login first.")
#     else:
#         st.error("Failed to fetch playlists.")




# # SUMMARY DATA
# if st.button("Get Artists"):
#     headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
#     response = requests.get(f"{API_BASE_URL}/me/top/artists", headers=headers)
#     st.write(response.status_code)

#     if response.status_code == 200:
#         artists = response.json().get('items', [])
#         for artist in artists:
#             if st.button(f"🎵 {artist['name']} ({artist['tracks']['total']} tracks)"):
#                 st.write(f"{artist['tracks']}")
#                 # for track in tracks:
#                 #         st.write(f"🎵 {track['name']} ({track['tracks']['total']} tracks)")

#     elif response.status_code == 401:
#         st.error("You are not logged in. Please login first.")
#     else:
#         st.error("Failed to fetch artists.")