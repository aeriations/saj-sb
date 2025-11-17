
import os
import asyncio

import discord
from discord.ext import commands

import dctoken

prefix = '>'
client = commands.Bot(command_prefix=prefix, self_bot=True)


TOKEN = dctoken.token()

@client.event
async def on_ready():
    print(f"""
        READY ->
          CLIENT: {client.user}
          PREFIX: {prefix}
    """)

async def load_cogs():
    for file_name in os.listdir('src/cogs'):
        if file_name.endswith('.py'):
            cog = f'cogs.{file_name[:-3]}'
            try:
                await client.load_extension(cog)
            except Exception as e:
                print(f"{e}")

async def main():
    async with client:
        await load_cogs()
        await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())