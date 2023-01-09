import discord

from pathlib import Path

import asyncio
import sys
import requests
import json

isDownloading = False


def get_cogs(cog_path: str) -> list[str]:
    cog_path = Path(cog_path)

    if cog_path.is_file():
        return [Path(cog_path).with_suffix("").as_posix().replace("/", ".")]
    return [
        (path.with_suffix("").as_posix().replace("/", "."))
        for path in cog_path.rglob("*.py")
    ]


async def isnt_slash_owner(interaction, reason, bot):
    app_info = await bot.application_info()
    if interaction.user.id == app_info.owner.id:
        return False
    embed = discord.Embed(
        title="Your command was not executed.",
        description=reason,
        color=0xf24f4f
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
    return True


def seconds_to_string(seconds):
    seconds = int(seconds)
    minutes = (seconds % 3600) // 60
    seconds %= 60
    return f"{minutes}:0{seconds}" if seconds < 10 else f"{minutes}:{seconds}"


async def asynclyrun(code):
    # Create the subprocess; redirect the standard output
    # into a pipe.
    proc = await asyncio.create_subprocess_exec(
        sys.executable, '-c', code,
        stdout=asyncio.subprocess.PIPE)

    # Read one line of output.
    data = await proc.stdout.readline()
    line = data.decode('ascii').rstrip()

    # Wait for the subprocess exit.
    await proc.wait()
    return line


def scrape_info_from_video(id):
    # getting the request from url
    r = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={id}&part=snippet&key=AIzaSyBYsYGCEURlPFacyhiuQKvfgUvCVZiWBOI")

    # turn r.text into json
    r = json.loads(r.text)

    return r['items'][0]['snippet']

