from pyrogram import Client, filters
from player import join_vc, skip_vc

@Client.on_message(filters.command("play"))
async def play_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /play [song/url]")

    query = " ".join(message.command[1:])
    stream = await join_vc(message.chat.id, query)
    await message.reply(f"▶️ Playing: **{stream['title']}**")

@Client.on_message(filters.command("skip"))
async def skip_handler(client, message):
    stream = await skip_vc(message.chat.id)
    if stream:
        await message.reply(f"⏭ Skipped, now playing: **{stream['title']}**")
    else:
        await message.reply("❌ Nothing left in queue.")
