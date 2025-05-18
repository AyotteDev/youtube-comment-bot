# YouTube Comment Bot

An educational project demonstrating how to automate posting comments on YouTube videos using the YouTube Data API. This tool shows how to authenticate with OAuth, interact with the YouTube API, and automate tasks with Python.

**Created by:** Dennis Ayotte / The Captain Dumbass™

---

## 🎓 Educational Purpose

This project is designed to demonstrate:
- OAuth 2.0 authentication flow
- YouTube Data API usage
- Python automation techniques
- Proper API credential handling
- Scheduled task execution with cron

It's intended for learning purposes and as a starting point for your own projects.

---

## ✨ Features

- Authenticates using OAuth 2.0 (client_secret.json required)
- Scans your most recent YouTube uploads (configurable number)
- Posts random comments from a customizable template list
- Designed for **personal channels** only (does not spam)
- Built for **macOS**, includes a cron-friendly shell wrapper
- Logs actions to a `/logs` folder

---

## 🚀 Setup Instructions

### 1. Enable the YouTube Data API
- Visit the [Google Cloud Console](https://console.cloud.google.com/)
- Create a project (or reuse an existing one)
- Enable **YouTube Data API v3**

### 2. Create OAuth Credentials
- Go to **APIs & Services > Credentials**
- Click "Create Credentials" → choose **OAuth client ID**
- Choose **Desktop App** and download your `client_secret.json` file
- Place it in the root of this project directory

### 3. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### 4. First-Time Authentication
```bash
python youtube_comment_bot.py
```

This opens a browser window to grant access to your channel.  
> **IMPORTANT:** Use Google Chrome as your default browser. Safari does not work properly with the OAuth flow.

After approval, it stores `token.json` for future runs.

### 5. Customize Comments
Edit the `comments.txt` file to include your own comments (one per line).

---

## 🔁 Automation (macOS Cron)

Use the included `run_comment_bot.sh` script. Example crontab entry:
```cron
30 15 * * 1-5 /path/to/youtube-comment-bot/run_comment_bot.sh >> /path/to/youtube-comment-bot/logs/cron_output.log 2>&1
```

> Adjust time as needed. This example runs Mon–Fri at 3:30 PM.

Not familiar with cron? See the included [cron_guide.md](cron_guide.md) for detailed instructions on setting up scheduled tasks on macOS.

---

## 🛡️ Security

- Do **not** share your `client_secret.json` or `token.json`.
- They are ignored via `.gitignore` by default.
- Never push them to GitHub or public storage.
- Be aware of YouTube API quota limitations.

---

## ⚠️ Legal / Use Disclaimer

This project is provided for **educational purposes only**.

It is your responsibility to:
- Follow [YouTube's Terms of Service](https://www.youtube.com/t/terms)
- Follow [YouTube's API Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- Follow [YouTube's Community Guidelines](https://www.youtube.com/howyoutubeworks/policies/community-guidelines/)
- Be aware of [YouTube API Quota limitations](https://developers.google.com/youtube/v3/getting-started#quota)

Misuse of this script may result in channel penalties or API bans. Use responsibly and only on your own content.

---

## 📄 License

MIT License — see `LICENSE` file for full details.

Copyright (c) 2025 Dennis Ayotte / The Captain Dumbass™
