import discord
from discord import app_commands
from discord.ext import commands

from etc.functions import scrape_info_from_video, asynclyrun, isnt_slash_owner

import asyncio
import json
import re

Skip = False
Stop = False

with open("config.json") as f:
    config = json.load(f)


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leave", description="Leaves the voice channel")
    async def leave(self, ctx):
        await ctx.response.send_message("disconnected :D", ephemeral=True, delete_after=30)
        await ctx.guild.voice_client.disconnect()

    @app_commands.command(name="play", description="Play music from a youtube url")
    async def play(self, ctx, query: str):
        if ctx.user.voice is None:
            return await ctx.response.send_message("enter a voice channel stupid.", ephemeral=True, delete_after=30)
        if ctx.guild.voice_client is None:
            await ctx.user.voice.channel.connect()
        if ctx.guild.voice_client.is_playing():
            return await ctx.response.send_message("You can't overwrite the currently playing song!")
        if query.endswith(".mp3"):
            embed = discord.Embed(
                title="Now Playing",
                description=
                f"""
                URL: Local File
                Title: {query}
                """,
                color=0x4f4ff2
            )
            await ctx.response.send_message(embed=embed, delete_after=600)
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(f"stored_audio/{query}"))
            return
        videoregex = re.compile(r"^(?:https?://)?(?:www\.)?youtu(?:be\.com/watch\?v=([a-zA-Z0-9_\-]+)|\.be/([a-zA-Z0-9_\-]+))")
        if not (videomatch := videoregex.match(query)):
            return await ctx.response.send_message("Invalid youtube link or mp3 file!", ephemeral=True, delete_after=30)

        embed = discord.Embed(
            title="Working...",
            description="Downloading file to disk. (This might take a bit)\n...or i could just, y'know error.",
            color=0x4f4ff2
        )
        embed.set_footer(text=f"{query}")

        await ctx.response.send_message(embed=embed)

        with open("stored_audio/latest.txt", 'r') as f:
            lines = f.readlines()

        videoid = re.search(r"[a-zA-Z0-9_\-]+$", videomatch[0])[0]
        videodata = scrape_info_from_video(videoid)

        if videoid not in lines:
            await asynclyrun(
                "import yt_dlp as youtube_dl" + "\nydl_opts = {'outtmpl': 'stored_audio/audio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}" + "\nwith youtube_dl.YoutubeDL(ydl_opts) as ydl:" + f"\n    ydl.download('{query}')")

        ctx.guild.voice_client.play(discord.FFmpegPCMAudio("stored_audio/audio.mp3"))

        thumbnails = videodata["thumbnails"]

        with open('stored_audio/latest.txt', 'w') as f:
            f.write(videoid)

        embed = discord.Embed(
            title="Now Playing",
            description=
            f"""
            URL: {query}
            Title: {videodata["title"]}
            Author: {videodata["channelTitle"]}
            """,
            color=0x4f4ff2
        )

        keys = ["maxres", "standard"]
        for key in keys:
            if key in thumbnails:
                embed.set_image(url=thumbnails[key]["url"])
                break

        await ctx.edit_original_response(embed=embed)


async def setup(bot):
    print("Loaded Voice!")
    await bot.add_cog(Voice(bot))
