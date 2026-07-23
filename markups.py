from telegram import InlineKeyboardButton, InlineKeyboardMarkup

PAGE_SIZE=15

def create_track_buttons(index):
    keyboard = [
        [
            InlineKeyboardButton(
                "▶ Find Match",
                callback_data=f"match:{index}"
            ),
            InlineKeyboardButton(
                "📥 Download",
                callback_data=f"download:{index}"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

def create_playlist_buttons(tracks,page):
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    page_tracks = tracks[start:end]

    keyboard=[]

    for i, track in enumerate(page_tracks, start=start + 1):
        keyboard.append([InlineKeyboardButton(f"🎵 {track['name']}", callback_data=f"song:{i}")])

    return keyboard

def create_playlist_markup(tracks, page):
    keyboard = create_playlist_buttons(tracks, page)

    total_pages = (len(tracks)-1)//PAGE_SIZE + 1

    nav = []

    if page > 0:
        nav.append(
            InlineKeyboardButton(
                "⬅ Prev",
                callback_data=f"page:{page-1}"
            )
        )

    nav.append(
        InlineKeyboardButton(
            f"{page+1}/{total_pages}",
            callback_data="ignore"
        )
    )

    if page < total_pages-1:
        nav.append(
            InlineKeyboardButton(
                "Next ➡",
                callback_data=f"page:{page+1}"
            )
        )

    keyboard.append(nav)

    keyboard.append([
        InlineKeyboardButton(
            "📦 Download Entire Playlist",
            callback_data="download_playlist"
        )
    ])

    return InlineKeyboardMarkup(keyboard)
