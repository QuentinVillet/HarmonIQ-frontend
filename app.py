import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, jsonify
from dotenv import load_dotenv
import secrets
import os
import pandas as pd
import json
import time
from flask_session import Session
import os


# Load environment variables
load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = os.getenv('redirect_uri')
scope = "playlist-modify-private user-library-read playlist-read-private"


# App config
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session' # TBD
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the server
app.config['SESSION_PERMANENT'] = False    # Make sessions non-permanent
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_session')  # Directory for session files
Session(app)


@app.route('/login')
def login():
    session.clear()
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return jsonify({"auth_url": auth_url})


@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    try:
        token_info = sp_oauth.get_access_token(code)
        session["token_info"] = token_info
        # Redirect back to Streamlit with a success indicator
        return redirect(f"http://localhost:8502/?success=true&token={token_info['access_token']}")  # Replace with Streamlit URL
    except Exception as e:
        print(f"Authorization error: {e}")
        return redirect(f"http://localhost:8502/?success=false")


@app.route('/logout')
def logout():
    session.clear()
    for key in list(session.keys()):
        session.pop(key)
    return jsonify({'session status': 'succesfully logged out.'})


@app.route('/playlists')
def get_playlists():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401
    access_token = auth_header.split(" ")[1]

    sp = spotipy.Spotify(auth=access_token)
    playlists = sp.current_user_playlists(limit=50)
    # playlists = [{'name':item['name'], 'id':item['id']} for item in results['items']]
    return jsonify(playlists)

# if not token_valid:
    #     print("Invalid token. Redirecting to login.")
    #     return redirect("/")

@app.route('/favTracks')
def get_user_tracks():
    # Check if token is valid
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401
    access_token = auth_header.split(" ")[1]

    sp = spotipy.Spotify(auth=access_token)
    try:
        results = sp.current_user_saved_tracks(limit=50)
        tracks = [item['track']['id'] for item in results['items']]
        return json.dumps(tracks, indent=4)
    except Exception as e:
        print(f"Error fetching tracks: {e}")
        return "An error occurred. Please try again."


def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # No token in session
    if not token_info:
        return {}, token_valid

    # Check if token is expired
    now = int(time.time())
    is_token_expired = token_info.get('expires_at', 0) - now < 60

    if is_token_expired:
        sp_oauth = create_spotify_oauth()
        try:
            token_info = sp_oauth.refresh_access_token(token_info.get('refresh_token'))
            session['token_info'] = token_info
            token_valid = True
        except Exception as e:
            print(f"Error refreshing token: {e}")
            session.clear()  # Clear session if token refresh fails
            return {}, False
    else:
        token_valid = True

    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=url_for('authorize', _external=True),
            scope=scope,
            show_dialog=True)

if __name__ == "__main__":
    app.run(debug=True)





# OLDER VERSION


# @app.route('/login')
# def login():
#     session.clear()
#     sp_oauth = create_spotify_oauth()
#     auth_url = sp_oauth.get_authorize_url()
#     print(auth_url)
#     return redirect(auth_url)


# @app.route('/authorize')
# def authorize():
#     sp_oauth = create_spotify_oauth()
#     session.clear()  # Clear session for a fresh login
#     code = request.args.get('code')
#     try:
#         token_info = sp_oauth.get_access_token(code)
#         session["token_info"] = token_info
#         print("Token obtained successfully.")
#         return redirect('/getPlaylists')
#     except Exception as e:
#         print(f"Authorization error: {e}")
#         return "Authorization failed. Please try again."


# @app.route('/logout')
# def logout():
#     session.clear()
#     for key in list(session.keys()):
#         session.pop(key)
#     return redirect('/')

# @app.route('/getPlaylists')
# def get_user_playlists():
#      # Check if token is valid
#     token_info, token_valid = get_token()
#     print(f"Session token: {session.get('token_info')}, Token valid: {token_valid}")
#     if not token_valid:
#         print("Invalid token. Redirecting to login.")
#         return redirect("/")  # Redirect to login to reauthorize

#     # Use the token to fetch data
#     sp = spotipy.Spotify(auth=token_info['access_token'])
#     try:
#         results = sp.current_user_playlists(limit=50, offset=0)
#         tracks = [{'name':item['name'], 'id':item['id']} for item in results['items']]
#         return json.dumps(tracks, indent=4)
#     except Exception as e:
#         print(f"Error fetching tracks: {e}")
#         return "An error occurred. Please try again."


# @app.route('/getTracks')
# def get_user_tracks():
#     # Check if token is valid
#     token_info, token_valid = get_token()
#     if not token_valid:
#         print("Invalid token. Redirecting to login.")
#         return redirect("/")  # Redirect to login to reauthorize

#     # Use the token to fetch data
#     sp = spotipy.Spotify(auth=token_info['access_token'])
#     try:
#         results = sp.current_user_saved_tracks(limit=10)
#         tracks = [item['track']['id'] for item in results['items']]
#         return json.dumps(tracks, indent=4)
#     except Exception as e:
#         print(f"Error fetching tracks: {e}")
#         return "An error occurred. Please try again."


# def get_token():
#     token_valid = False
#     token_info = session.get("token_info", {})

#     # No token in session
#     if not token_info:
#         return {}, token_valid

#     # Check if token is expired
#     now = int(time.time())
#     is_token_expired = token_info.get('expires_at', 0) - now < 60

#     if is_token_expired:
#         sp_oauth = create_spotify_oauth()
#         try:
#             token_info = sp_oauth.refresh_access_token(token_info.get('refresh_token'))
#             session['token_info'] = token_info
#             token_valid = True
#         except Exception as e:
#             print(f"Error refreshing token: {e}")
#             session.clear()  # Clear session if token refresh fails
#             return {}, False
#     else:
#         token_valid = True

#     return token_info, token_valid


# def create_spotify_oauth():
#     return SpotifyOAuth(
#             client_id=client_id,
#             client_secret=client_secret,
#             redirect_uri=url_for('authorize', _external=True),
#             scope=scope,
#             show_dialog=True)

# if __name__ == "__main__":
#     app.run(debug=True)


# Checks to see if token is valid and gets a new token if not
# def get_token():
#     token_valid = False
#     token_info = session.get("token_info", {})

#     # Checking if the session already has a token stored
#     if not (session.get('token_info', False)):
#         token_valid = False
#         return token_info, token_valid

#     # Checking if token has expired
#     now = int(time.time())
#     is_token_expired = session.get('token_info').get('expires_at') - now < 60

#     # Refreshing token if it has expired
#     if (is_token_expired):
#         sp_oauth = create_spotify_oauth()
#         token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

#     token_valid = True
#     return token_info, token_valid
