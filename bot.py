from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from config import BOT_TOKEN, OWNER_ID, LOG_CHANNEL
from database import save_start_image, get_start_image
from utils import start_buttons

# Dictionary to track which user is sending image for /set_image
waiting_for_image = {}

# Initialize bot
bot = Client("AutoFilterBot", bot_token=BOT_TOKEN)

# /start command
@bot.on_message(filters.command("start") & (filters.private | filters.group))
async def start_cmd(client, message):
    text = f'“**Hi {message.from_user.first_name}\nI am a advance auto filter. I can help you to find anime & series if I have in my database.**”\n\nMaintained By @AniWorld_Bots_Hub'
    file_id = get_start_image()
    if file_id:
        await message.reply_photo(photo=file_id, caption=text, reply_markup=start_buttons())
    else:
        await message.reply(text, reply_markup=start_buttons())

# /set_image command
@bot.on_message(filters.command("set_image") & filters.user(OWNER_ID))
async def set_image_cmd(client, message):
    waiting_for_image[message.from_user.id] = True
    await message.reply("📸 Send me the image you want to save as start image.")

# Handle photo upload for start image
@bot.on_message(filters.photo)
async def save_image(client, message):
    if waiting_for_image.get(message.from_user.id):
        file_id = message.photo.file_id
        save_start_image(file_id)
        waiting_for_image.pop(message.from_user.id)
        await message.reply("✅ Start image saved successfully!")

# /filter command (admin only)
@bot.on_message(filters.command("filter") & filters.user(OWNER_ID))
async def filter_cmd(client, message):
    await message.reply("Usage:\nReply to a message and type: /filter keyword")

# Auto filter in private or group
@bot.on_message(filters.text & (filters.private | filters.group))
async def auto_filter(client, message):
    text = message.text.lower()
    # Example: if user sends "jujutsu kaisen"
    if "jujutsu kaisen" in text:
        await message.reply("🔍 Found Jujutsu Kaisen in database!")

# Start the bot
bot.run()
