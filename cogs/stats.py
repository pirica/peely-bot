import asyncio
import random

import aiohttp
import discord
from discord.ext import commands

from Settings import SETTINGS
from modules import footer
from modules import sql


class stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx, *, name: str = None):
        msg = await ctx.send(embed=discord.Embed(color=SETTINGS.embedcolor, description=f"Stats are loading."))
        if name is None:
            temp = await sql.c()
            dbuser = temp[0]
            db = temp[1]
            await db.execute("SELECT * FROM statsuser WHERE id=%s", (ctx.author.id,))
            id = await db.fetchone()
            if not id:
                await db.execute("SELECT * FROM users WHERE discord_id=%s", (ctx.author.id,))
                id = await db.fetchone()
            await db.close()
            dbuser.close()
            if not id:
                return await msg.edit(embed=discord.Embed(description=f"You must Tag a user or write a Ingame Name",
                                                          color=SETTINGS.embederror))
        elif ctx.message.mentions:
            temp = await sql.c()
            dbuser = temp[0]
            db = temp[1]
            await db.execute("SELECT * FROM statsuser WHERE id=%s", (ctx.message.mentions[0].id,))
            id = await db.fetchone()
            if not id:
                await db.execute("SELECT * FROM users WHERE discord_id=%s", (ctx.author.id,))
                id = await db.fetchone()
            await db.close()
            dbuser.close()
            if not id:
                return await msg.edit(
                    embed=discord.Embed(title="This user doesnt exist in my Database.", color=SETTINGS.embederror))
            name = None
        try:
            if id:
                print(id[1])
                id = id[1]
            elif name:
                print(name)
            else:
                print("Gar nichts ??!???")
        except:
            pass
        embed = discord.Embed(color=SETTINGS.embedsuccess)
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"Please select a Input Device.")
        embed.add_field(name="All", value=f"🌐", inline=True)
        embed.add_field(name="Keyboard", value=f"⌨️", inline=True)
        embed.add_field(name="Gamepad", value=f"🎮", inline=True)
        embed.add_field(name="Touchscreen", value=f"📱", inline=True)
        await msg.edit(embed=embed)
        await msg.add_reaction("🌐")
        await msg.add_reaction("⌨️")
        await msg.add_reaction("🎮")
        await msg.add_reaction("📱")

        payload = await self.client.wait_for("raw_reaction_add", timeout=60,
                                             check=lambda p: p.user_id == ctx.author.id and p.message_id == msg.id)

        embed = discord.Embed(color=SETTINGS.embedsuccess)
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"Stats for {name}")
        if str(payload.emoji) == "⌨️":
            type = "keyboardMouse"
        elif str(payload.emoji) == "🎮":
            type = "gamepad"
        elif str(payload.emoji) == "📱":
            type = "touch"
        else:
            type = "all"
        if name is not None:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://fortnite-api.com/v1/stats/br/v2?name={name}&image={type}") as data:
                    if data.status == 404:
                        embed = discord.Embed(title=f"Sorry, this Account doesnt exist. Error: {data.status}",
                                              color=SETTINGS.embederror)
                        return await msg.edit(embed=embed)
                    elif data.status == 429:
                        while True:
                            async with aiohttp.ClientSession() as cs:
                                async with cs.get(
                                        f"https://fortnite-api.com/v1/stats/br/v2?name={name}&image={type}") as data:
                                    if data.status == 429:
                                        await asyncio.sleep(random.randint(1.00, 2.59))
                                        continue
                                    else:
                                        break
                    elif data.status == 403:
                        embed = discord.Embed(color=SETTINGS.embederror,
                                              title=f"Unfortunately, due to {name} account settings, I am unable to access the statistics. This can be changed in the account settings.")
                        embed.set_image(url="https://i.imgur.com/l0c6VIb.gif")
                        embed.set_footer(text=await footer.get_footer())
                        return await msg.edit(embed=embed)
                    elif data.status != 200:
                        embed = discord.Embed(
                            title=f"Sorry, the Fortnite-API is currently not reachable. Please try again "
                                  f"later. Error: {data.status}", color=SETTINGS.embederror)
                        return await msg.edit(embed=embed)
                    try:
                        response = await data.json()
                    except Exception as ex:
                        embed = discord.Embed(
                            title=f"Sorry, the Fortnite-API is currently not reachable. Please try again "
                                  f"later.", description=f"Error: ``{ex}``", color=SETTINGS.embederror)
                        return await msg.edit(embed=embed)
        else:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://fortnite-api.com/v1/stats/br/v2/{id}?image={type}") as data:
                    if data.status == 404:
                        embed = discord.Embed(title=f"Sorry, this Account doesnt exist. Error: {data.status}",
                                              color=SETTINGS.embederror)
                        return await msg.edit(embed=embed)
                    elif data.status == 429:
                        while True:
                            async with aiohttp.ClientSession() as cs:
                                async with cs.get(
                                        f"https://fortnite-api.com/v1/stats/br/v2?name={name}&image={type}") as data:
                                    if data.status == 429:
                                        await asyncio.sleep(random.randint(1.0000, 2.5000))
                                        continue
                                    else:
                                        break
                    elif data.status == 403:
                        embed = discord.Embed(color=SETTINGS.embederror,
                                              title=f"Unfortunately, due to {name} account settings, I am unable to access the statistics. This can be changed in the account settings.")
                        embed.set_image(url="https://i.imgur.com/l0c6VIb.gif")
                        embed.set_footer(text=await footer.get_footer())
                        return await msg.edit(embed=embed)
                    elif data.status != 200:
                        embed = discord.Embed(
                            title=f"Sorry, the Fortnite-API is currently not reachable. Please try again "
                                  f"later. Error: {data.status}", color=SETTINGS.embederror)
                        return await msg.edit(embed=embed)
                    try:
                        response = await data.json()
                    except Exception as ex:
                        embed = discord.Embed(
                            title=f"Sorry, the Fortnite-API is currently not reachable. Please try again "
                                  f"later.", description=f"Error: ``{ex}``", color=SETTINGS.embederror)
                        return await msg.edit(embed=embed)
        embed = discord.Embed(color=SETTINGS.embedcolor)
        embed.set_author(name=f"Stats for " + response["data"]["account"]["name"], icon_url=ctx.author.avatar_url,
                         url="https://peely.de")
        embed.set_image(url=response["data"]["image"])
        embed.set_footer(text=await footer.get_footer())
        await msg.clear_reactions()
        await msg.edit(embed=embed)

    @commands.command(aliases=["set", "setingamename"])
    async def setingname(self, ctx, *, ing):
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://fortnite-api.com/v1/stats/br/v2?name={ing}") as data:
                    if data.status == 404:
                        return await ctx.send(
                            embed=discord.Embed(description=f"I cannot find the Account with the name ``{ing}``",
                                                color=SETTINGS.embederror))
                    elif data.status != 200:
                        return await ctx.send(
                            embed=discord.Embed(
                                description=f"Dear was an error with the Fortnite-API. ``{data.status}`` Please try it later.",
                                color=SETTINGS.embederror))
                    try:
                        data = await data.json()
                        id = str(data["data"]["account"]["id"])
                    except:
                        pass
            if id is None:
                return await ctx.send(
                    embed=discord.Embed(description=f"I cannot find the Account with the name ``{ing}``",
                                        color=SETTINGS.embederror))
            temp = await sql.c()
            user = temp[0]
            db = temp[1]
            await db.execute("DELETE FROM statsuser WHERE id=%s", (ctx.author.id,))
            await db.execute("INSERT INTO statsuser VALUE (%s, %s)", (ctx.author.id, id,))
            await user.commit()
            await db.close()
            user.close()
            embed = discord.Embed(color=SETTINGS.embedsuccess)
            embed.set_author(icon_url=ctx.author.avatar_url,
                             name=f"I have successfully linked your ingame name ({ing}) to your Discord account ({ctx.author.display_name}).")
            embed.set_footer(text=await footer.get_footer())
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(stats(client))
