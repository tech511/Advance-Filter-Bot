from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Channel", url="https://t.me/AniWorld_Zone"),
                InlineKeyboardButton("Developer", url="https://t.me/H_IN_AT_A")
            ]
        ]
    )
