import boto3
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

BUCKET = "playlist-pirate-tele"


def song_exists(spotify_id):

    key = f"songs/{spotify_id}.mp3"

    try:
        s3.head_object(
            Bucket=BUCKET,
            Key=key
        )
        return True

    except:
        return False


def upload_song(
    spotify_id,
    file_path
):
    key = f"songs/{spotify_id}.mp3"

    s3.upload_file(
        file_path,
        BUCKET,
        key
    )

    return key


def download_song(
    spotify_id,
    output_path
):
    key = f"songs/{spotify_id}.mp3"

    s3.download_file(
        BUCKET,
        key,
        output_path
    )

    return output_path