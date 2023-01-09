
import discord
from discord.ext import commands
from discord import app_commands

import asyncio


class OnPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # when the bot is pinged do something funny
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.bot.user.mentioned_in(message):
            await self.bot.change_presence(activity=discord.Game(name=f"FUCK, {message.author.name}"))
            await asyncio.sleep(1)
            await self.bot.change_presence()
            return


async def setup(bot):
    print("Loaded OnPing!")
    await bot.add_cog(OnPing(bot))
