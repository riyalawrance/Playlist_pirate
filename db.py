import sqlite3

DB_NAME = "songs.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        spotify_id TEXT PRIMARY KEY,
        title TEXT,
        artist TEXT,
        s3_key TEXT,
        telegram_file_id TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_song(spotify_id, title, artist, s3_key, file_id=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO songs
    (spotify_id, title, artist, s3_key, telegram_file_id)
    VALUES (?, ?, ?, ?, ?)
    """, (spotify_id, title, artist, s3_key, file_id))

    conn.commit()
    conn.close()

def get_song(spotify_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM songs
    WHERE spotify_id = ?
    """, (spotify_id,))

    result = cursor.fetchone()

    conn.close()

    return result

def update_telegram_file_id(
    spotify_id,
    telegram_file_id
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE songs
    SET telegram_file_id=?
    WHERE spotify_id=?
    """, (
        telegram_file_id,
        spotify_id
    ))

    conn.commit()
    conn.close()