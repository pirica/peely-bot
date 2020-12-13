import aiohttp
import discord
from discord.ext import commands

import Settings.SETTINGS


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


def setup(client):
    client.add_cog(news(client))
