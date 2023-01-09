import json

import discord
from discord.ext import commands

from etc.functions import get_cogs


class Bot(commands.Bot):

    async def setup_hook(self):
        for cog in get_cogs("cogs"):
            await self.load_extension(cog)


with open("config.json") as f:
    config = json.load(f)

bot = Bot(
    command_prefix=config["legacy_prefix"],
    intents=discord.Intents.all(),
    case_insensitive=True
)


@bot.command()
async def sync(ctx):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Game(name="Syncing..."), status=discord.Status.idle)
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="Synced!"), status=discord.Status.online)

if __name__ == "__main__":
    bot.run(config["token"])
