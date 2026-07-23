import os
import tempfile
import shutil

from db import get_song, save_song
from aws_storage import song_exists, download_song, upload_song
from yt import search_youtube, download_audio


def sanitize(name):
    invalid = '<>:"/\\|?*'
    for ch in invalid:
        name = name.replace(ch, "_")
    return name


def fetch_song(track, folder):
    spotify_id = track["id"]
    title = track["name"]
    artist = track["artist"]

    output_file = os.path.join(
        folder,
        sanitize(f"{artist} - {title}.mp3")
    )

    cached = get_song(spotify_id)

    if cached and song_exists(spotify_id):
        print(f"S3 HIT : {title}")
        download_song(spotify_id, output_file)
        return output_file

    print(f"Downloading : {title}")

    result = search_youtube(title, artist)

    temp = download_audio(result["url"])

    shutil.move(temp, output_file)

    s3_key = upload_song(
        spotify_id,
        output_file
    )

    save_song(
        spotify_id,
        title,
        artist,
        s3_key
    )

    return output_file


def build_playlist_folder(tracks):
    folder = tempfile.mkdtemp(prefix="playlist_")

    for track in tracks:
        try:
            fetch_song(track, folder)
        except Exception as e:
            print(track["name"], e)

    return folder

import zipfile


def make_zip(folder):

    zip_path = folder + ".zip"

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for file in os.listdir(folder):

            full = os.path.join(folder, file)

            zipf.write(
                full,
                arcname=file
            )

    return zip_path