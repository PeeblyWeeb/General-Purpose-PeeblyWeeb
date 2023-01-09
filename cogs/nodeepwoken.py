import datetime

import discord
from discord.ext import commands
from discord import app_commands


class NoDeepwoken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # When someone joins a specific voice channel timeout the user instantly
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            return
        if before.channel == after.channel:
            return
        if after.channel.id == 1055983389007683775:
            try:
                await member.timeout(datetime.datetime.now().astimezone() + datetime.timedelta(minutes=5))
            except discord.errors.Forbidden:
                print("User was too high in the hierarchy to be timed out.")
            return


async def setup(bot):
    print("Loaded NoDeepwoken!")
    await bot.add_cog(NoDeepwoken(bot))
