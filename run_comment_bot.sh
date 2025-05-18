#!/bin/bash

# YouTube Comment Bot Runner
# This script runs the YouTube comment bot using the virtual environment
# It's designed for use with macOS cron or manual execution
#
# IMPORTANT PREREQUISITES:
# 1. You must have already created a Python virtual environment in a 'venv' folder
# 2. You must have installed the required packages in this environment:
#    pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
# 3. You must have placed client_secret.json in the same directory as this script
# 4. Google Chrome should be set as your default browser (Safari doesn't work with OAuth)
# 5. FIRST-TIME SETUP: Run the Python script directly first (python youtube_comment_bot.py)
#    to complete the authentication process in your browser before using this script with cron
#
# Example crontab entry (runs Monday-Friday at 3:30 PM):
# 30 15 * * 1-5 /path/to/youtube-comment-bot/run_comment_bot.sh

# Navigate to the script directory (so relative paths work)
cd "$(dirname "$0")"

# Activate the Python virtual environment (must be created beforehand)
source venv/bin/activate

# Run the main Python script
python youtube_comment_bot.py
