from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

from spotipy_api import get_playlist_tracks, get_album_tracks, get_tracks
from markups import *
from yt import *
from db import *
from aws_storage import *

from dotenv import load_dotenv
import os
load_dotenv()

playlist_cache = {}

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(f"Hello {name}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "spotify.com/playlist/" in text:
        playlist_id = (text.split("/playlist/")[1].split("?")[0])
        await update.message.reply_text(f"Playlist ID:\n{playlist_id}")
        await update.message.reply_text("Fetching playlist... 🎧")

        tracks = get_playlist_tracks(playlist_id)
        if not tracks:
            await update.message.reply_text("No tracks found ❌")
            return

        chat_id = update.effective_chat.id

        playlist_cache[chat_id] = { "tracks": tracks, "current_page": 0}
        
        await update.message.reply_text("🎵 Select a song", reply_markup=create_playlist_markup(tracks, 0))

    elif "spotify.com/album/" in text:
        album_id = (text.split("/album/")[1].split("?")[0])
        await update.message.reply_text(f"Album ID:\n{album_id}")
        await update.message.reply_text("Fetching album... 🎧")

        tracks = get_album_tracks(album_id)
        if not tracks:
            await update.message.reply_text("No tracks found ❌")
            return

        chat_id = update.effective_chat.id

        playlist_cache[chat_id] = { "tracks": tracks, "current_page": 0}

        await update.message.reply_text("🎵 Select a song", reply_markup=create_playlist_markup(tracks, 0))


    # elif "spotify.com/track/" in text:
    #     track_id = (text.split("/track/")[1].split("?")[0])
    #     await update.message.reply_text(f"Track ID:\n{track_id}")

    #     tracks=get_tracks(track_id)
    #     if not tracks:
    #         await update.message.reply_text("No track found ❌")
    #         return
        
    #     track = tracks[0]
    #     message = f"{track['name']} - {track['artist']}"
    #     reply_markup = create_song_buttons(track)
    #     await update.message.reply_text(message,reply_markup=reply_markup)
    else:
        await update.message.reply_text("Send a Spotify playlist or track link.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "ignore":
        return

    chat_id = query.message.chat.id
    playlist_data = playlist_cache.get(chat_id)
    if not playlist_data:
        return
    tracks = playlist_data["tracks"]

    if data.startswith("page:"):
        page = int(data.split(":")[1])
        playlist_data["current_page"] = page

        await query.edit_message_text(
            "Select a song",
            reply_markup=create_playlist_markup(page, len(tracks))
        )
    
    elif data.startswith("song:"):
        index = int(data.split(":")[1])-1
        track = tracks[index]

        result = search_youtube(track["name"], track["artist"])

        await query.message.reply_text(
            f"🎵 {track['name']}\n"
            f"👤 {track['artist']}\n\n",
            reply_markup=create_track_buttons(index)
            )

    elif data.startswith("match:"):
        index = int(data.split(":")[1])

        track = tracks[index]

        result = search_youtube(
        track["name"],
        track["artist"]
        )

        await query.message.reply_text(
            f"📺 Match Found\n {result['title']}\n\n{result['url']}"
        )

    elif data.startswith("download:"):
        
        index = int(data.split(":")[1])

        track = tracks[index]
        spotify_id = track["id"]
        title = track["name"]
        artist = track["artist"]

        cached = get_song(spotify_id)

        if cached:

            telegram_file_id = cached[4]

            if telegram_file_id:

                print("TELEGRAM CACHE HIT")

                await query.message.reply_audio(
                    audio=telegram_file_id
                )

                return
        
        temp_file = f"temp/{spotify_id}.mp3"

        os.makedirs("temp", exist_ok=True)

        try:

            # Song exists in DB -> download from S3
            if cached and song_exists(spotify_id):

                print("S3 CACHE HIT")

                download_song(
                    spotify_id,
                    temp_file
                )

            else:

                print("CACHE MISS")

                result = search_youtube(
                    title,
                    artist
                )

                temp_file = download_audio(
                    result["url"]
                )

                s3_key = upload_song(
                    spotify_id,
                    temp_file
                )

                save_song(
                    spotify_id=spotify_id,
                    title=title,
                    artist=artist,
                    s3_key=s3_key
                )

            # Send audio to Telegram
            with open(temp_file, "rb") as audio:

                msg = await query.message.reply_audio(
                    audio=audio,
                    title=title,
                    performer=artist
                )

            telegram_file_id = msg.audio.file_id

            update_telegram_file_id(
                spotify_id,
                telegram_file_id
            )

            print("SUCCESS")

        except Exception as e:

            print("ERROR:", e)

        finally:

            if os.path.exists(temp_file):
                os.remove(temp_file)

    elif data=="download_playlist":
        await query.message.reply_text(
            "📥 Preparing playlist...\nThis may take a few minutes."
        )

        from playlist_zip import build_playlist_folder, make_zip
        import shutil

        folder = build_playlist_folder(tracks)

        zip_path = make_zip(folder)

        print(f"{os.path.getsize(zip_path)/1024/1024:.2f} MB")

        with open(zip_path, "rb") as f:
            await query.message.reply_document(
                document=f,
                filename="playlist.zip",
                write_timeout=300,
                read_timeout=300
            )

        shutil.rmtree(folder)

        os.remove(zip_path)

app = (
    Application.builder()
    .token(TOKEN)
    .read_timeout(120)
    .write_timeout(120)
    .connect_timeout(120)
    .pool_timeout(120)
    .build()
)

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.add_handler(CallbackQueryHandler(button_callback))

init_db()

app.run_polling()