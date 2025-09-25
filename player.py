import os
import asyncio
from collections import defaultdict

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

from imageio_ffmpeg import get_ffmpeg_exe
import ytdl  # Assumed helper module using yt-dlp (must provide an async fetch, see below)
import config  # contains API_ID, API_HASH, SESSION (string session or path)

# === Ensure ffmpeg executable is available via imageio_ffmpeg ===
ffmpeg_path = get_ffmpeg_exe()  # bundled ffmpeg binary path2
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

# === Initialize Pyrogram Client and PyTg
client = Client("userbot", api_id=config.API_ID, api_hash=config.API_HASH, session_string=config.SESSION)
client.start()

pytgcalls = PyTgCalls(client)
pytgcalls.start()

# Per-chat queues and current track titles
queues = defaultdict(list)  # chat_id -> list of (stream_url, title)
current_track = {}         # chat_id -> title of currently playing track

# == Event: when a track ends, play the next or leave ==
@pytgcalls.on_stream_end()
async def _on_stream_end(_, update):
    chat_id = update.chat_id
    if queues[chat_id]:
        # Pop next track and play it
        next_url, next_title = queues[chat_id].pop(0)
        current_track[chat_id] = next_title
        await pytgcalls.join_group_call(
            chat_id,
            stream=AudioPiped(next_url)
        )
    else:
        # No more tracks; clear state and leave VC
        current_track[chat_id] = None
        queues.pop(chat_id, None)
        try:
            await pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass  # Ignore if already not in a call

async def join_vc(chat_id: int, query: str):
    """
    Join or play in voice chat: fetch stream for `query`, then play or enqueue it.
    Returns the track title (playing now or queued).
    """
    try:
        # Fetch audio stream URL and title from ytdl helper
        stream_url, title = await ytdl.get_audio(query)
    except Exception as e:
        # Could not fetch a valid stream
        raise RuntimeError(f"Error fetching stream: {e}")

    # If nothing is currently playing in this chat, start immediately
    if current_track.get(chat_id) is None:
        current_track[chat_id] = title
        # Ensure a queue exists (it may be empty)
        queues[chat_id] = queues.get(chat_id, [])
        try:
            await pytgcalls.join_group_call(
                chat_id,
                stream=AudioPiped(stream_url)
            )
        except Exception as e:
            current_track[chat_id] = None
            raise RuntimeError(f"Failed to join voice chat: {e}")
        return title
    else:
        # Already playing: add to queue
        queues[chat_id].append((stream_url, title))
        return title  # queued title

async def skip_vc(chat_id: int):
    """
    Skip current track in the voice chat. Plays next track if available.
    Returns the title of the new track, or None if queue is empty.
    """
    if current_track.get(chat_id) is None:
        return None  # Nothing to skip
    
    if queues.get(chat_id):
        # There is a next track queued
        next_url, next_title = queues[chat_id].pop(0)
        current_track[chat_id] = next_title
        try:
            # Restart the call with the next stream
            await pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        try:
            await pytgcalls.join_group_call(
                chat_id,
                stream=AudioPiped(next_url)
            )
        except Exception as e:
            current_track[chat_id] = None
            raise RuntimeError(f"Failed to play next track: {e}")
        return next_title
    else:
        # No more tracks: end call
        current_track[chat_id] = None
        queues.pop(chat_id, None)
        try:
            await pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        return None
