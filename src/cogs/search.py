import discord
from discord.ext import commands

import aiohttp

import asyncio

PLATFORMS = {
    "GitHub": lambda u: f"https://github.com/{u}",
    "X": lambda u: f"https://x.com/{u}",
    "Reddit": lambda u: f"https://www.reddit.com/user/{u}",
    "Instagram": lambda u: f"https://www.instagram.com/{u}/",
    "TikTok": lambda u: f"https://www.tiktok.com/@{u}",
    "Twitch": lambda u: f"https://www.twitch.tv/{u}",
    "YouTube": lambda u: f"https://www.youtube.com/@{u}",
    "Facebook": lambda u: f"https://www.facebook.com/{u}",
    "Pinterest": lambda u: f"https://www.pinterest.com/{u}/",
    "Steam": lambda u: f"https://steamcommunity.com/id/{u}",
    "SoundCloud": lambda u: f"https://soundcloud.com/{u}",
    "Medium": lambda u: f"https://medium.com/@{u}",
    "DeviantArt": lambda u: f"https://www.deviantart.com/{u}",
    "Roblox": lambda u: f"https://www.roblox.com/user.aspx?username={u}",
    "GitLab": lambda u: f"https://gitlab.com/{u}",
    "Kaggle": lambda u: f"https://www.kaggle.com/{u}",
    "Patreon": lambda u: f"https://www.patreon.com/{u}",
    "Letterboxd": lambda u: f"https://letterboxd.com/{u}/",
    "BuyMeACoffee": lambda u: f"https://www.buymeacoffee.com/{u}",
    "Flickr": lambda u: f"https://www.flickr.com/photos/{u}/",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

async def load(msg, main: str):
    for i in range(2):
        await msg.edit(".")
        await asyncio.sleep(0.1)
        await msg.edit("..")
        await msg.edit("...")
    await msg.edit(main)

_semaphore = asyncio.Semaphore(6)
async def check_url(session: aiohttp.ClientSession, url):
    try:
        async with session.get(url, allow_redirects=True, timeout=8) as resp:
            txt = (await resp.text())[:5000]

            final_url = str(resp.url)
            status = resp.status

            if status == 404:
                return False
            
            bad_url = ["/login", "/signup", "/404", "/notfound", "/error", "/help"]
            if any(path in final_url.lower() for path in bad_url):
                return False
            
            bad_signals = [
                "page not found",
                "user not found",
                "couldn't find this account",
                "this page isn't available",
                "profile not found",
                "no such user",
                "404"
            ]

            if any(sig in txt.lower() for sig in bad_signals):
                return False
            
            return True
        
    except aiohttp.ClientError:
        return False
    except asyncio.TimeoutError:
        return False
    except Exception as e:
        print(f"[ERROR]: {e}")
        return False

class search_cog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded {__name__}")

    @commands.command()
    async def search_user(self, ctx: commands.Context, username: str):
        await ctx.message.delete()
        
        handle = username.strip()
        if not handle:
            await ctx.send("provide non-empty username.", delete_after=1)
        elif len(handle) > 64:
            await ctx.send("username is too long (over 64 chars)", delete_after=1)

        to_check = PLATFORMS.copy()

        found = []
        not_found = []
        error = []

        async with aiohttp.ClientSession(headers=HEADERS) as session:
            tasks = []

            for name, f in to_check.items():
                url = f(handle)
                async def make_probe(n=name, u=url):
                    async with _semaphore:
                        exists = await check_url(session, u)
                        return (n, u, exists)
                
                tasks.append(make_probe())
            
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in results:
                    if isinstance(result, Exception):
                        error.append(("unknown", str(result)))
                    else:
                        name, url, exists = result
                        if exists:
                            found.append((name, url))
                        else:
                            not_found.append((name, url))
        
        def format_list(lst):
            if not lst:
                return "None"
            return "\n    ".join(f"{name}: {url}" for name, url in lst)

        text = f"""
    FOUND ->
        {format_list(found)}

    NOT FOUND ->
        {format_list(not_found)}

    ERROR ->
        {format_list(error)}
        \n-# DISCLAIMER: false positives + negatives do happen."""

        # Send the message
        message = await ctx.send("...")
        await load(message, text)



async def setup(client):
    await client.add_cog(search_cog(client))