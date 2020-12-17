import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS as SETTINGS
from modules import sql


class leaks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.checkleaks.start()
        except:
            self.checkleaks.stop()
            self.checkleaks.start()

    @commands.command()
    async def leaks(self, ctx):
        embed = discord.Embed(color=SETTINGS.embedcolor, description="Leaks")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.peely.de/v1/leaks') as data:
                url = (await data.json())['uniqueurl']
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @tasks.loop(seconds=10)
    async def checkleaks(self):
        try:
            CachedLeaks = json.loads(
                await (await aiofiles.open('Cache/peelyleaks.json', mode='r')).read())  # Load the cached store
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.peely.de/v1/leaks') as data:
                if data.status != 200:
                    return
                Leaks = await data.json()
        if CachedLeaks['time'] != Leaks['time'] and int(data.status) == 200:
            await (await aiofiles.open('Cache/peelyleaks.json', mode='w+')).write(
                json.dumps(Leaks, indent=2))  # Overwrite the old store
            print("New Leaks")
            if SETTINGS.test is True:
                print("TEST MODUS LEAKS")
                return

            await self.post_leak(url=Leaks['uniqueurl'])

    async def post_leak(self, url: str):
        temp = await sql.c()
        myuser = temp[0]
        mydb = temp[1]
        await mydb.execute("SELECT * FROM leaks", )
        data = await mydb.fetchall()
        await mydb.execute("DELETE FROM lastleaks")
        for g in data:
            guild = self.client.get_guild(g[0])
            if not isinstance(guild, discord.Guild):
                continue
            channel = guild.get_channel(g[1])
            if channel:
                try:
                    embed = discord.Embed(color=SETTINGS.embedcolor, title=f"New Cosmetics detected!")
                    embed.set_image(url=url)
                    msg = await channel.send(embed=embed)
                    await mydb.execute("INSERT INTO lastleaks VALUE (%s, %s)", (channel.id, msg.id,))
                except Exception as ex:
                    print(ex)
                    continue
            else:
                continue
        await mydb.close()
        myuser.close()

    @commands.command()
    async def deletelastleaks(self, ctx):
        if SETTINGS.nono != ctx.author.id:
            return
        else:
            user, db = await sql.c()
            await db.execute("SELECT * FROM lastleaks")
            data = await db.fetchall()
            await db.execute("DELETE FROM lastleaks")
            await user.commit()
            await db.close()
            user.close()
            for i in data:
                try:
                    cha = self.client.get_channel(i[0])
                    msg = await cha.fetch_message(i[1])
                    await msg.delete()
                except:
                    continue

    def cog_unload(self):
        self.checkleaks.stop()
        print("shop LOOP BEENDET")
        try:
            self.client.unload_extension("cogs.leaks")
        except:
            print("CANOT UNLOAD EXTENSION leaks")
        try:
            self.client.load_extension("cogs.leaks")
        except:
            print("CANOT RELOAD EXTENSION leaks")


def setup(client):
    client.add_cog(leaks(client))
