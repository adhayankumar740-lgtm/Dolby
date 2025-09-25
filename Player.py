from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from pyrogram import Client
import asyncio
from config import API_ID, API_HASH, SESSION_NAME
from ytdl import get_stream

userbot = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(userbot)

queues = {}  # {chat_id: [tracks...]}

async def join_vc(chat_id, query):
    stream = get_stream(query)
    queues.setdefault(chat_id, []).append(stream)

    if not pytgcalls.get_call(chat_id):
        await pytgcalls.join_group_call(
            chat_id,
            InputStream(InputAudioStream(stream["url"]))
        )
    else:
        # if already in VC, play next
        pass
    return stream

async def skip_vc(chat_id):
    if chat_id in queues and len(queues[chat_id]) > 1:
        queues[chat_id].pop(0)
        stream = queues[chat_id][0]
        await pytgcalls.change_stream(
            chat_id,
            InputStream(InputAudioStream(stream["url"]))
        )
        return stream
    return None
