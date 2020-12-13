import random

import aiohttp
import discord
from discord.ext import commands

from Settings import SETTINGS
from modules import footer, paginator


async def check(ctx):
    try:
        await ctx.message.delete()
    except Exception as ex:
        print("No rights!", ex)
        pass
    if ctx.author.id == SETTINGS.nono:
        return True
    else:
        return False


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="Get a Joke")
    async def joke(self, ctx):
        async with ctx.typing():
            nummer = random.randint(1, 2)
            if nummer == 1:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://icanhazdadjoke.com/slack') as data:
                        json = await data.json()
                if data.status != 200:
                    return await ctx.send(embed=discord.Embed(description="There was an Error with the API."))
                joke = ""
                url = ""
                for i in json["attachments"]:
                    joke += str(i["text"])
                    url += str(i["footer"])
                    break
                url = url.split(" - ")
                url = url[0].split("<")
                url = url[1].split(">")
                print(str(url[0]))
                embed = discord.Embed(description=joke, color=SETTINGS.embedcolor)
                embed.set_author(icon_url="https://i.ibb.co/hFMdgcT/smile-1.png", name=f"Here is a joke.",
                                 url=str(url[0]))
                embed.set_footer(text=await footer.get_footer())
                await ctx.send(embed=embed)
            elif nummer == 2:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://api.chucknorris.io/jokes/random') as data:
                        json = await data.json()
                if data.status != 200:
                    return await ctx.send(embed=discord.Embed(description="There was an Error with the API."))
                embed = discord.Embed(description=json["value"], color=SETTINGS.embedcolor)
                embed.set_author(icon_url=json["icon_url"], name=f"Here is a Chuck Norris fact.")
                embed.set_footer(text=await footer.get_footer())
                await ctx.send(embed=embed)

    @commands.command(usage="Get the daily picture of the NASA.")
    async def nasapic(self, ctx):
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://api.nasa.gov/planetary/apod?api_key=mdZ8bbl4hZqUzWqcg6sMkdgRUqaIeUR8oJhk6yPF') as data:
                    json = await data.json()
            embed = discord.Embed(color=SETTINGS.embedcolor, title=json["title"])
            try:
                embed.set_image(url=json["hdurl"])
            except:
                try:
                    embed.add_field(name="URL:", value=json["url"])
                except:
                    pass
            await ctx.send(embed=embed)
            await paginator.TextPages(ctx=ctx, text=json["explanation"].replace("  ", "\n")).paginate()

    @commands.command(usage="Get an random picture of the Mars.")
    async def marspic(self, ctx):
        async with ctx.typing():
            msg = await ctx.send(random.choice(
                ["Loading a picture from the mars", "Contact NASA", "Contact Space Shuttle", "Contact aliens"]))
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key'
                                  '=mdZ8bbl4hZqUzWqcg6sMkdgRUqaIeUR8oJhk6yPF') as data:
                    json = await data.json()
            data = random.choice(json["photos"])
            embed = discord.Embed(color=SETTINGS.embedcolor, title="Picture from the Mars")
            embed.set_image(url=data["img_src"])
            await msg.edit(content=None, embed=embed)

    @commands.command(usage="Get an random fact of cats.")
    async def catfact(self, ctx):
        async with ctx.typing():
            msg = await ctx.send("Loading a fact")
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://cat-fact.herokuapp.com/facts/random') as data:
                    json = await data.json()
            embed = discord.Embed(color=SETTINGS.embedcolor, description=json["text"])
            await msg.edit(content=None, embed=embed)


def setup(client):
    client.add_cog(fun(client))
