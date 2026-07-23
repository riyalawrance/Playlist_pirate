import yt_dlp
import os

def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "128",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info)
        mp3_file = os.path.splitext(filename)[0] + ".mp3"

        return mp3_file

def search_youtube(track_name, artist):
    query = f"{track_name} {artist}"

    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        results = ydl.extract_info(
            f"ytsearch1:{query}",
            download=False
        )

    video = results["entries"][0]

    return {
        "title": video["title"],
        "url": video["webpage_url"]
    }
