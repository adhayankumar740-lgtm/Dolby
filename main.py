import os
from pyrogram import Client, filters
from ntgcalls import PyTgCalls
from ntgcalls.types.input_stream import InputAudioStream
from ntgcalls.types.input_stream.quality import HighQualityAudio

# Load configuration from environment variables
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ.get("BOT_TOKEN")   # For bot
SESSION = os.environ["SESSION"]           # String session for userbot
CHAT_ID = int(os.environ.get("CHAT_ID", 0))  # Optional fixed chat

# Pyrogram clients
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

# VC client (ntgcalls)
voice = PyTgCalls(user)

# Song queue
queue = {}

# -------- Commands -------- #
@bot.on_message(filters.command("play"))
async def cmd_play(_, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])

    if not query:
        return await message.reply_text("❌ Please give a song name or link.")

    # Example: Instead of yt-dlp here, just a placeholder file
    stream = InputAudioStream(
        "example.mp3",  # replace with yt-dlp downloaded file or URL
        HighQualityAudio()
    )

    if chat_id not in queue or not voice.is_connected(chat_id):
        await voice.join_group_call(chat_id, stream)
        queue[chat_id] = []
        await message.reply_text(f"▶️ Playing: {query}")
    else:
        queue[chat_id].append(stream)
        await message.reply_text(f"➕ Added to queue: {query}")


@bot.on_message(filters.command("skip"))
async def cmd_skip(_, message):
    chat_id = message.chat.id
    if queue.get(chat_id):
        next_track = queue[chat_id].pop(0)
        await voice.change_stream(chat_id, next_track)
        await message.reply_text("⏭ Skipped to next track.")
    else:
        await voice.leave_group_call(chat_id)
        await message.reply_text("✅ Queue empty, left VC.")


@bot.on_message(filters.command("pause"))
async def cmd_pause(_, message):
    await voice.pause_stream(message.chat.id)
    await message.reply_text("⏸ Paused.")


@bot.on_message(filters.command("resume"))
async def cmd_resume(_, message):
    await voice.resume_stream(message.chat.id)
    await message.reply_text("▶️ Resumed.")


@bot.on_message(filters.command("stop"))
async def cmd_stop(_, message):
    await voice.leave_group_call(message.chat.id)
    await message.reply_text("🛑 Stopped & left VC.")


# -------- Startup -------- #
async def main():
    await user.start()
    await bot.start()
    await voice.start()
    print("✅ Music bot is running...")
    await bot.idle()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
