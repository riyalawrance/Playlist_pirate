# 🏴‍☠️ Playlist Pirate

**Plunder your favorite Spotify playlists and albums straight into Telegram — as MP3s, on demand.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/badge/Spotify-API-1DB954?style=for-the-badge&logo=spotify&logoColor=white" alt="Spotify">
  <img src="https://img.shields.io/badge/AWS-S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white" alt="AWS S3">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/riyalawrance/Playlist_pirate?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/issues/riyalawrance/Playlist_pirate?style=flat-square" alt="Open Issues">
  <img src="https://img.shields.io/github/stars/riyalawrance/Playlist_pirate?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/last-commit/riyalawrance/Playlist_pirate?style=flat-square" alt="Last Commit">
</p>

---

## 📖 About

**Playlist Pirate** is a cloud-powered Telegram bot that lets you send a Spotify playlist or album link and get back playable MP3s — no manual searching, no repeated downloads. It fetches accurate track metadata from the Spotify API, locates the best match on YouTube, downloads and converts the audio, and caches everything across **SQLite → Amazon S3 → Telegram File ID** so repeat requests are served almost instantly.

---

## ✨ Features

- 🎵 Accepts Spotify **playlist** and **album** links
- 📃 Retrieves complete track metadata using the Spotify API
- 📄 Displays tracks with **paginated inline Telegram menus**
- 🔍 Searches YouTube for the best matching song
- 🎧 Downloads audio from YouTube and converts it to **MP3**
- ☁️ Stores downloaded songs in **Amazon S3** for persistent caching
- 🗄️ Maintains song metadata and cache info using **SQLite**
- ⚡ Uses **Telegram File ID caching** to instantly resend previously delivered songs without re-uploading
- 📥 Downloads songs directly from S3 when available, avoiding repeated YouTube downloads
- 🧹 Automatically cleans up temporary files after processing
- 🚀 Multi-level caching strategy (**SQLite → S3 → Telegram cache**) that reduces bandwidth and download time

---

## 🛠️ Tech Stack

| Category                | Technology                                  |
|--------------------------|----------------------------------------------|
| Language                 | Python 3.10+                                 |
| Telegram Bot Framework   | `python-telegram-bot`                        |
| Spotify Integration      | Spotipy (Spotify Web API)                    |
| YouTube Search/Download  | `yt-dlp`                                      |
| Audio Processing         | FFmpeg                                        |
| Cloud Storage            | Amazon S3 (Boto3)                            |
| Database                 | SQLite                                        |
| Environment Management   | python-dotenv                                |
| APIs Used                | Spotify Web API, Telegram Bot API, Amazon S3 API |
| Deployment                | Local machine, VPS, or cloud server          |

---

## ✅ Prerequisites

Before you begin, make sure you have:

- Python 3.10 or higher
- FFmpeg installed and available on your system `PATH`
- A Telegram Bot Token (create one via [@BotFather](https://t.me/BotFather))
- A Spotify Developer account with:
  - Client ID
  - Client Secret
  - Redirect URI
- An AWS account with:
  - An S3 bucket
  - Access Key ID
  - Secret Access Key
- An active internet connection (required for Spotify, YouTube, Telegram, and AWS services)

---

## 🚀 Getting Started / Installation

### 1. Clone the repository

```bash
git clone https://github.com/riyalawrance/Playlist_pirate.git
cd Playlist_pirate
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Dependencies include: `python-telegram-bot`, `spotipy`, `yt-dlp`, `boto3`, `python-dotenv`

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token

CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=your_spotify_redirect_uri

AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_s3_bucket_name
```

### 5. Run the bot locally

```bash
python bot.py
```

You should see a confirmation in your terminal that the bot has started polling for messages.

---

## 💬 Usage

1. Open Telegram and start a chat with your bot.
2. Send `/start` to initialize the bot.
3. Paste a **Spotify playlist or album link**, for example:

```text
   https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
```

4. The bot fetches all tracks and displays them in a **paginated inline menu**.
5. Tap a track to download it — the bot will:
   - Check Telegram File ID cache → send instantly if found
   - Check S3 cache → download from S3 if found
   - Otherwise, search YouTube, download, convert to MP3, upload to S3, and send it to you

### Example Commands

| Command   | Description                          |
|-----------|---------------------------------------|
| `/start`  | Initializes the bot and shows a welcome message |
| `/help`   | Displays usage instructions          |
| *(paste link)* | Fetches and lists tracks from a Spotify playlist/album |

---

## 🤝 Contributing

Contributions are welcome and appreciated! To contribute:

1. **Fork** the repository
2. Create a new branch
```bash
   git checkout -b feature/your-feature-name
```
3. Make your changes and commit them
```bash
   git commit -m "Add: your feature description"
```
4. Push to your fork
```bash
   git push origin feature/your-feature-name
```
5. Open a **Pull Request** describing your changes

Please open an issue first for major changes to discuss what you'd like to modify. Make sure to follow existing code style and add comments where helpful.

---

## 📜 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for full details.

---

<p align="center">Made with ⚓ and a love for music by <a href="https://github.com/riyalawrance">riyalawrance</a></p>
