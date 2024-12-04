import streamlit as st
import spotipy



@st.cache_data
def get_playlists():

    st.query_params.update(page="playlist")
    st.title("Welcome to your playlist generator !")

    if st.button("show my playlists"):
        sp = spotipy.Spotify(auth=st.session_state['access_token'])
        results = sp.current_user_playlists(limit=50)
        playlists = [{'name':item['name'], 'id':item['id']} for item in results['items']]
        for playlist in playlists:
            st.write(f'{playlist["name"]} ({playlist["id"]})')




# def playlist_generator():


# # Store selected playlist details
# if "selected_playlists" not in st.session_state:
#     st.session_state.selected_playlists = []

# if st.session_state.access_token:
#     playlists = fetch_playlists(st.session_state.access_token)

#     # Display playlists and allow the user to select
#     if playlists:
#         st.write("Playlists:")
#         for playlist in playlists:
#             playlist_id = playlist["id"]
#             playlist_name = playlist["name"]
#             track_count = playlist["tracks"]["total"]

#             # Add button for each playlist
#             if st.button(f"🎵 {playlist_name} ({track_count} tracks)", key=playlist_id):
#                 # Cache the id and name of the playlist
#                 st.session_state.selected_playlists.append({"id": playlist_id, "name": playlist_name})
#                 st.success(f"Added playlist '{playlist_name}' to the cache!")
#     else:
#         st.write("No playlists found.")

# # Display cached playlists
# if st.session_state.selected_playlists:
#     st.write("Cached Playlists:")
#     for saved_playlist in st.session_state.selected_playlists:
#         st.write(f"🎵 {saved_playlist['name']}")
