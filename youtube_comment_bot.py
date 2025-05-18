#!/usr/bin/env python3
"""
YouTube Comment Bot

This script automatically posts comments on your YouTube videos using the YouTube Data API.
It's designed for educational purposes to demonstrate API usage and automation.

== SETUP REQUIREMENTS ==
1. Create a project in Google Cloud Console (https://console.cloud.google.com/)
2. Enable the YouTube Data API v3 for your project
3. Create OAuth credentials (Desktop app) and download as 'client_secret.json'
4. Place the client_secret.json file in the same directory as this script
5. Set Google Chrome as your default browser (Safari doesn't work properly with OAuth)
6. Run this script once to authenticate (browser window will open)
7. After authentication, a token.json file will be created for future use

== CUSTOMIZATION ==
- Edit comments.txt to change the comment templates
- Adjust MAX_VIDEOS_TO_CHECK below to scan more or fewer videos
- See README.md for more detailed instructions
"""

import os
import random
import datetime
import logging
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ----------------------------------------
# CONFIGURATION
# ----------------------------------------

# === USER CONFIGURABLE SETTINGS ===

# Number of recent videos to check and potentially comment on
# Increase this number to scan more videos, decrease to scan fewer
MAX_VIDEOS_TO_CHECK = 7

# === SYSTEM PATHS AND AUTHENTICATION ===

# Required OAuth 2.0 scope for managing YouTube comments
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Define base directory and key file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File containing your comment templates (one per line)
# This file should already exist with your desired comments
COMMENTS_FILE = os.path.join(BASE_DIR, 'comments.txt')

# OAuth token storage - will be created automatically after first authentication
# DO NOT create this file manually
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

# OAuth client secrets file - YOU MUST DOWNLOAD THIS from Google Cloud Console
# See setup instructions in the README or the header comment of this script
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'client_secret.json')

# Directory for storing log files - created automatically
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# ----------------------------------------
# SETUP LOGGING
# ----------------------------------------

# Create log directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Create a timestamped log file
log_filename = f"log_{datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.txt"
logging.basicConfig(filename=os.path.join(LOG_DIR, log_filename), level=logging.INFO)

# ----------------------------------------
# YOUTUBE AUTHENTICATION
# ----------------------------------------

def authenticate_youtube():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This will open a browser window the first time for OAuth approval
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('youtube', 'v3', credentials=creds)

# ----------------------------------------
# CORE FUNCTIONS
# ----------------------------------------

def get_my_channel_id(youtube):
    """Fetch the authenticated user's channel ID."""
    response = youtube.channels().list(part='id', mine=True).execute()
    return response['items'][0]['id']

def get_recent_video_ids(youtube, channel_id, max_results=MAX_VIDEOS_TO_CHECK):
    """Get a list of the most recent video IDs from the uploads playlist."""
    uploads_playlist_id = youtube.channels().list(
        part='contentDetails', id=channel_id
    ).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    playlist_items = youtube.playlistItems().list(
        part='snippet', maxResults=max_results, playlistId=uploads_playlist_id
    ).execute()

    return [item['snippet']['resourceId']['videoId'] for item in playlist_items['items']]

def load_comment_templates():
    """Read and clean the list of possible comments from file."""
    with open(COMMENTS_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def comment_exists(youtube, video_id, comment_templates, channel_id):
    """Check if one of the template comments already exists on the video."""
    comments_response = youtube.commentThreads().list(
        part='snippet', videoId=video_id, maxResults=100, textFormat='plainText'
    ).execute()

    for item in comments_response.get('items', []):
        top_comment = item['snippet']['topLevelComment']['snippet']
        if top_comment['authorChannelId']['value'] == channel_id:
            comment_text = top_comment['textDisplay']
            if any(template in comment_text for template in comment_templates):
                return True
    return False

def post_comment(youtube, video_id, comment):
    """Post a selected comment to a given video."""
    body = {
        'snippet': {
            'videoId': video_id,
            'topLevelComment': {
                'snippet': {
                    'textOriginal': comment
                }
            }
        }
    }
    youtube.commentThreads().insert(part='snippet', body=body).execute()
    logging.info(f"Posted comment to video: {video_id}")

# ----------------------------------------
# MAIN EXECUTION
# ----------------------------------------

def main():
    youtube = authenticate_youtube()
    channel_id = get_my_channel_id(youtube)
    comment_templates = load_comment_templates()
    video_ids = get_recent_video_ids(youtube, channel_id)

    for vid in video_ids:
        if not comment_exists(youtube, vid, comment_templates, channel_id):
            chosen_comment = random.choice(comment_templates)
            post_comment(youtube, vid, chosen_comment)
            logging.info(f"Commented on video {vid}: {chosen_comment}")
        else:
            logging.info(f"Skipped video {vid}: matching comment already exists")

if __name__ == '__main__':
    main()
