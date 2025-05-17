import asyncio
import os
import re
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from Reex.utils.database import is_on_off
from Reex.utils.formatters import time_to_seconds

cook = "youtube_cookies.txt"


async def shell_cmd(cmd: str) -> str:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    err_decoded = err.decode("utf-8").lower()
    if err and "unavailable videos are hidden" not in err_decoded:
        return err.decode("utf-8")
    return out.decode("utf-8")


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = False) -> bool:
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption or ""
                        return text[entity.offset : entity.offset + entity.length]
            if message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = False):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        results = VideosSearch(link, limit=1)
        res = await results.next()
        if "result" not in res or not res["result"]:
            raise ValueError("Video tidak ditemukan")
        result = res["result"][0]

        title = result["title"]
        duration_min = result["duration"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        vidid = result["id"]

        duration_sec = 0
        if duration_min:
            duration_sec = int(time_to_seconds(duration_min))

        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = False):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        results = VideosSearch(link, limit=1)
        res = await results.next()
        if "result" not in res or not res["result"]:
            return None
        return res["result"][0]["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = False):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        results = VideosSearch(link, limit=1)
        res = await results.next()
        if "result" not in res or not res["result"]:
            return None
        return res["result"][0]["duration"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = False):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        results = VideosSearch(link, limit=1)
        res = await results.next()
        if "result" not in res or not res["result"]:
            return None
        return res["result"][0]["thumbnails"][0]["url"].split("?")[0]

    async def video(self, link: str, videoid: Union[bool, str] = False):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        else:
            return 0, stderr.decode()

    async def playlist(self, link: str, limit: int, user_id: int, videoid: Union[bool, str] = False):
        if videoid:
            link = self.listbase + link
        link = link.split("&")[0]

        playlist = await shell_cmd(
            f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        result = [key for key in playlist.split("\n") if key]
        return result

    async def track(self, link: str, videoid: Union[bool, str] = False):
        try:
            if videoid:
                link = self.base + link
            link = link.split("&")[0]

            results = VideosSearch(link, limit=1)
            res = await results.next()
            if "result" not in res or not res["result"]:
                raise ValueError("Tidak ada hasil video ditemukan.")
            result = res["result"][0]

            track_details = {
                "title": result["title"],
                "link": result["link"],
                "vidid": result["id"],
                "duration_min": result["duration"],
                "thumb": result["thumbnails"][0]["url"].split("?")[0],
            }
            return track_details, result["id"]
        except Exception as e:
            print(f"Error pada fungsi track: {e}")
            return None, None

    async def formats(self, link: str, videoid: Union[bool, str] = False):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            r = ydl.extract_info(link, download=False)
            formats_available = []
            for fmt in r.get("formats", []):
                if "dash" in fmt.get("format", "").lower():
                    continue
                if not all(key in fmt for key in ("format", "filesize", "format_id", "ext", "format_note")):
                    continue
                formats_available.append(
                    {
                        "format": fmt["format"],
                        "filesize": fmt["filesize"],
                        "format_id": fmt["format_id"],
                        "ext": fmt["ext"],
                        "format_note": fmt["format_note"],
                        "yturl": link,
                    }
                )
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = False):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        a = VideosSearch(link, limit=10)
        res = await a.next()
        result = res.get("result")
        if not result or len(result) <= query_type:
            raise IndexError("Query type index out of range in slider results.")
        item = result[query_type]

        title = item["title"]
        duration_min = item["duration"]
        vidid = item["id"]
        thumbnail = item["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = False,
        videoid: Union[bool, str] = False,
        songaudio: Union[bool, str] = False,
        songvideo: Union[bool, str] = False,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> Union[tuple[str, bool], None]:
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "cookiefile": cook,
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
            return info

        def video_dl():
            ydl_opts = {
                "format": f"{format_id}",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "quiet": True,
                "nocheckcertificate": True,
                "geo_bypass": True,
                "cookiefile": cook,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
            return info

        try:
            if songaudio:
                info = await loop.run_in_executor(None, audio_dl)
                filename = f"downloads/{info['id']}.mp3"
                if os.path.isfile(filename):
                    return filename, True
                else:
                    return None, False

            elif songvideo:
                info = await loop.run_in_executor(None, video_dl)
                ext = info.get("ext", "")
                filename = f"downloads/{info['id']}.{ext}"
                if os.path.isfile(filename):
                    return filename, True
                else:
                    return None, False
            elif video:
                ydl_opts = {
                    "format": "best[height<=?720][width<=?1280]",
                    "outtmpl": "downloads/%(id)s.%(ext)s",
                    "quiet": True,
                    "nocheckcertificate": True,
                    "geo_bypass": True,
                    "cookiefile": cook,
                }

                def generic_video_dl():
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        return ydl.extract_info(link, download=True)

                info = await loop.run_in_executor(None, generic_video_dl)
                ext = info.get("ext", "")
                filename = f"downloads/{info['id']}.{ext}"
                if os.path.isfile(filename):
                    return filename, True
                else:
                    return None, False
            else:
                return None, False
        except Exception as e:
            print(f"Error di download: {e}")
            return None, False
