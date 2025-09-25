import yt_dlp

ytdl_opts = {
    "format": "bestaudio/best",
    "quiet": True,
    "default_search": "auto",
    "source_address": "0.0.0.0"
}

ydl = yt_dlp.YoutubeDL(ytdl_opts)

def get_stream(query: str):
    info = ydl.extract_info(query, download=False)
    if "entries" in info:
        info = info["entries"][0]
    return {
        "title": info.get("title"),
        "url": info.get("url")
    }
