from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from player import userbot, pytgcalls
import handlers  # registers handlers
from keepalive import keepalive

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

if __name__ == "__main__":
    userbot.start()
    pytgcalls.start()
    keepalive()  # starts Flask server for Render
    bot.run()
