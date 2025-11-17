import discord
from discord.ext import commands

import asyncio
import random

async def load(msg, main: str):
    for i in range(2):
        await msg.edit(".")
        await asyncio.sleep(0.1)
        await msg.edit("..")
        await msg.edit("...")
    await msg.edit(main)

class misc_cog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.gifs = [
            "https://tenor.com/view/monkey-monkey-dancing-orangutan-monkey-dance-happy-monkey-gif-12702179649294906179",
            "https://tenor.com/view/oops-tease-smirk-smile-it-girl-gif-8678759334685550059",
            "https://tenor.com/view/giovrios-giovriod-monkey-monkey-tounge-gif-11786438347595686225",
            "https://tenor.com/view/wrizz-monkey-monkey-sigma-gif-14012962261800188400",
            "https://tenor.com/view/fat-fat-monkey-fat-monkey-smile-fat-monkey-smiling-monkey-gif-1768197236560593059",
            "https://tenor.com/view/monkey-tongue-monkey-lala-monkey-funny-gif-11438112160717212775",
            "https://cdn.discordapp.com/attachments/1204118760969998347/1204158659374882846/UniConverter_14_20230520214851.gif?ex=6905c1e4&is=69047064&hm=dbad7ad4b2640f257beb4aefcd2e8a8954b1b8ea12a350b298481e68a66c81b7"
        ]
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded {__name__}")

    @commands.command()
    async def monkey(self, ctx: commands.Context):
        await ctx.message.delete()
        gif = random.choice(self.gifs)

        await ctx.send("<@746454958764720178>")
        await ctx.send(gif)


async def setup(client):
    await client.add_cog(misc_cog(client))