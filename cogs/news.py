from datetime import datetime
import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands

import Settings.SETTINGS
from discord.ext import tasks

from modules import sql


class news(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def news(self, ctx):
        if ctx.invoked_subcommand is None:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://fortnite-api.com/v2/news/br',
                                  headers={"x-api-key": Settings.SETTINGS.FNAPIKEY}) as data:
                    News = await data.json()
            if News is None:
                nono = self.client.get_user(Settings.SETTINGS.nono)
                await nono.send("News (Offi API) not loaded", News)
                return
            if News["data"]["image"] is None:
                return await ctx.send(embed=discord.Embed(color=Settings.SETTINGS.embederror,
                                                          description=f"There are currently no News Ingame."))
            embed = discord.Embed(color=Settings.SETTINGS.embedcolor)
            embed.set_author(name=f"Battle Royale News",
                             icon_url="https://fortnite-api.com/assets/img/logo_small_128.png")
            img = News["data"]["image"]
            embed.set_image(url=f"{img}")
            await ctx.send(embed=embed)

    @news.command(usage="Get all BR News")
    async def br(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.peely.de/v1/br/news') as data:
                News = await data.json()
        if News["data"]["image"] is None:
            return await ctx.send(embed=discord.Embed(color=Settings.SETTINGS.embederror,
                                                      description=f"There are currently no News Ingame."))
        embed = discord.Embed(color=Settings.SETTINGS.embedcolor)
        embed.set_author(name=f"Battle Royale News", icon_url="https://fortnite-api.com/assets/img/logo_small_128.png")
        img = News["data"]["image"]
        embed.set_image(url=f"{img}")
        await ctx.send(embed=embed)

    @news.command(usage="Get all Creative News")
    async def creative(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.peely.de/v1/creative/news') as data:
                News = await data.json()
        if News["data"]["image"] is None:
            return await ctx.send(embed=discord.Embed(color=Settings.SETTINGS.embederror,
                                                      description=f"There are currently no News Ingame."))
        embed = discord.Embed(color=Settings.SETTINGS.embedcolor)
        embed.set_author(name=f"Creative News", icon_url="https://fortnite-api.com/assets/img/logo_small_128.png")
        img = News["data"]["image"]
        embed.set_image(url=f"{img}")
        await ctx.send(embed=embed)

    @news.command(usage="Get all STW News")
    async def stw(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.peely.de/v1/stw/news') as data:
                News = await data.json()
        if News["data"]["image"] is None:
            return await ctx.send(embed=discord.Embed(color=Settings.SETTINGS.embederror,
                                                      description=f"There are currently no News Ingame."))
        embed = discord.Embed(color=Settings.SETTINGS.embedcolor)
        embed.set_author(name=f"STW News", icon_url="https://fortnite-api.com/assets/img/logo_small_128.png")
        img = News["data"]["image"]
        embed.set_image(url=f"{img}")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.check_news.start()
        except:
            self.check_news.stop()
            self.check_news.start()

    @tasks.loop(seconds=5)
    async def check_news(self):
        await self.client.wait_until_ready()
        try:
            old = json.loads(await (await aiofiles.open('Cache/news.json', mode='r', errors='ignore')).read())
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://api.peely.de/v1/news') as data:
                    if data.status != 200:
                        return
                    new = await data.json()
        except Exception as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return
        for key in new["data"].keys():
            try:
                for newsd in new["data"][key]["motds"]:
                    if not newsd in old["data"][key]["motds"]:
                        if key == "creative":
                            if newsd in new["data"]["br"]["motds"]:
                                continue
                        user, db = await sql.c()
                        await db.execute("SELECT * FROM news")
                        data = await db.fetchall()
                        for send in data:
                            channel = self.client.get_channel(send[1])
                            if not channel:
                                continue
                            embed = discord.Embed(color=0x005500, title=str(key).upper() + " - " + newsd["title"],
                                                  description=news["body"])
                            embed.timestamp = datetime.utcnow()
                            embed.set_image(url=newsd["image"])
                            try:
                                await channel.send(embed=embed)
                            except:
                                continue
                        await db.close()
                        user.close()
            except:
                continue
        await (await aiofiles.open('Cache/news.json', mode='w+')).write(
            json.dumps(new, indent=2))

    def cog_unload(self):
        self.check_news.stop()
        print("shop LOOP BEENDET")
        try:
            self.client.unload_extension("cogs.news")
            self.client.load_extension("cogs.news")
        except:
            self.client.load_extension("cogs.news")
            print("CANOT RELOAD EXTENSION shop")


def setup(client):
    client.add_cog(news(client))
