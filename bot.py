from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from database import *

app = Client(
    "AutoFilterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

admins_waiting_image = set()

# ---------------- START ---------------- #

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    username = message.from_user.mention

    text = f"""
> **Hi {username}
> I am a advance auto filter.
> I can help you to find anime & series if I have in my database.**

Maintained By @AniWorld_Bots_Hub
"""

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Channel", url="https://t.me/AniWorld_Zone"),
            InlineKeyboardButton("Developer", url="https://t.me/H_IN_AT_A")
        ]]
    )

    image = await get_start_image()

    if image:
        await message.reply_photo(image, caption=text, reply_markup=buttons)
    else:
        await message.reply(text, reply_markup=buttons)

# ---------------- SET IMAGE (ADMIN ONLY) ---------------- #

@app.on_message(filters.command("set_image") & filters.user(OWNER_ID))
async def set_image_cmd(client, message):
    admins_waiting_image.add(message.from_user.id)
    await message.reply("📸 Send me the image you want to save as start image.")

@app.on_message(filters.photo & filters.private)
async def save_new_start_image(client, message):
    if message.from_user.id in admins_waiting_image:
        await set_start_image(message.photo.file_id)
        admins_waiting_image.remove(message.from_user.id)
        await message.reply("✅ Start image updated successfully!")

# ---------------- MANUAL FILTER ---------------- #

@app.on_message(filters.command("filter") & filters.user(OWNER_ID))
async def add_filter(client, message):
    try:
        _, keyword = message.text.split(" ", 1)
        reply = message.reply_to_message.text
        await add_manual_filter(keyword, reply)
        await message.reply("✅ Manual filter added.")
    except:
        await message.reply("Usage:\nReply to a message and type:\n/filter keyword")

# ---------------- AUTO FILTER GROUP ---------------- #

@app.on_message(filters.text & filters.group)
async def auto_filter(client, message):
    text = message.text.lower()

    manual = await check_manual_filter(text)
    if manual:
        await message.reply(manual["reply"])
        return

    result = await search_file(text)
    if result:
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📥 Get File", callback_data=result["file_id"])]]
        )
        await message.reply(
            "🔎 File Found! Click below to get.",
            reply_markup=button
        )

# ---------------- INLINE BUTTON HANDLER ---------------- #

@app.on_callback_query()
async def send_file_callback(client, callback_query):
    file_id = callback_query.data
    await callback_query.message.reply_document(file_id)
    await callback_query.answer()

# ---------------- SAVE FILE FROM GROUP ---------------- #

@app.on_message(filters.document | filters.video)
async def save_media(client, message):
    if message.chat.type in ["group", "supergroup"]:
        name = message.caption if message.caption else (
            message.document.file_name if message.document else "video"
        )
        file_id = message.document.file_id if message.document else message.video.file_id

        await save_file(name, file_id)

# ---------------- PRIVATE REACTION ---------------- #

@app.on_message(filters.private & filters.text)
async def private_react(client, message):
    if "jujutsu kaisen" in message.text.lower():
        await message.react("🔥")

# ---------------- LOG CHANNEL ---------------- #

@app.on_message(filters.all)
async def log_all(client, message):
    try:
        await message.forward(LOG_CHANNEL)
    except:
        pass

app.run()
