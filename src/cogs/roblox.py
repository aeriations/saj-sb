import discord
from discord.ext import commands

import requests
import json
import asyncio

async def load(msg, main: str):
    for i in range(2):
        await msg.edit(".")
        await asyncio.sleep(0.1)
        await msg.edit("..")
        await msg.edit("...")
    await msg.edit(main)


class roblox_cog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded {__name__}")

    @commands.command()
    async def get_roblox_user(self, ctx: commands.Context, user: str):
        await ctx.message.delete()
        req_body = {
            'usernames': [user],
            'excludeBannedUsers': False
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.post("https://users.roblox.com/v1/usernames/users", json.dumps(req_body), headers=headers)
        loads = json.loads(response.text)
        if len(loads['data']) == 0:
            return
        
        user_id = loads['data'][0]['id']
        response2 = requests.get(url=f"https://users.roblox.com/v1/users/{user_id}")
        jdata = response2.json()

        headshot = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={jdata.get('id')}&size=420x420&format=Png&isCircular=false&thumbnailType=HeadShot")
        hsdata = headshot.json()

        message = await ctx.send('...')
        await load(message, f"""```
            USER FOUND ->
                user: {jdata.get('name')}
                id: {jdata.get('id')}
                display: {jdata.get('displayName')}
                verified: {jdata.get('hasVerifiedBadge')}
                created: {jdata.get('created')}
                description: {jdata.get('description')}```
                {hsdata.get('data')[0]['imageUrl']}

        """)



async def setup(client):
    await client.add_cog(roblox_cog(client))