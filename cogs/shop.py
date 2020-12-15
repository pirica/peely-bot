import json
import traceback
from datetime import datetime

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import modules.paginator
from Settings import SETTINGS
from modules import sql


class shop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.checkstore.start()
        except:
            self.checkstore.stop()
            self.checkstore.start()
        try:
            self.fortniteapiupdate.start()
        except:
            self.fortniteapiupdate.stop()
            self.fortniteapiupdate.start()

    @commands.command(hidden=False, usage="Get the current Shop")
    async def shop(self, ctx):
        file = discord.File('Shop.png')
        embed = discord.Embed(color=0x009EFF)
        embed.set_author(name=f"Item Shop", icon_url="https://fortnite-api.com/assets/img/logo_small_128.png")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.peely.de/v1/shop') as data:
                url = (await data.json())['uniqueurl']
        embed.set_image(url=url)
        await ctx.send(embed=embed, file=file)

    @tasks.loop(seconds=10)
    async def checkstore(self):
        CachedStore = json.loads(
            await (await aiofiles.open('Cache/Store.json', mode='r')).read())  # Load the cached store
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.peely.de/v1/shop') as data:
                if data.status != 200:
                    return
                Store = await data.json()
        if CachedStore != Store:
            await (await aiofiles.open('Cache/Store.json', mode='w+')).write(
                json.dumps(Store, indent=2))  # Overwrite the old store
            print("New Shop")
            if SETTINGS.test is True:
                return
            now = datetime.now().strftime('%A %d %B %Y')
            user, db = await sql.c()
            await db.execute("SELECT * FROM shop")
            data = await db.fetchall()
            await db.execute("DELETE FROM lastshop")
            user.commit()
            for i in data:
                embed = discord.Embed(color=0x009EFF)
                embed.set_author(name=f"Item Shop from {now}", icon_url="https://fortnite-api.com/assets/img/logo_small_128.png",
                                 url=f"https://peely.de/")
                embed.set_image(url=f"{Store['uniqueurl']}")
                try:
                    channel = self.client.get_channel(i[1])
                    if channel:
                        try:
                            msg = await channel.send(embed=embed)
                            await db.execute("INSERT INTO lastshop VALUE (%s, %s)", (channel.id, msg.id,))
                            print("Image sent")
                        except Exception as ex:
                            print(ex)
                            continue
                    else:
                        continue
                except Exception as ex:
                    print(ex)
            await user.commit()
            await db.close()
            user.close()

    @tasks.loop(seconds=5)
    async def fortniteapiupdate(self):
        async with aiohttp.ClientSession() as session:
            resp = await session.get("https://fortnite-api.com/v2/shop/br?language=en")
            if resp.status != 200:
                return
            new = await resp.json()
            old = json.loads(
                await (await aiofiles.open('Cache/shopdata.json', mode='r')).read())
            try:
                if old['data']['hash'] != new['data']['hash']:
                    await (await aiofiles.open('Cache/shopdata.json', mode='w+')).write(
                        json.dumps(new, indent=2))
                    newitems = []
                    for i in new['data']['featured']['entries']:
                        for i2 in i['items']:
                            try:
                                i2['price'] = i['finalPrice']
                            except KeyError:
                                i2['price'] = 0
                            newitems.append(i2)
                    for i in new['data']['daily']['entries']:
                        for i2 in i['items']:
                            try:
                                i2['price'] = i['finalPrice']
                            except KeyError:
                                i2['price'] = 0
                            newitems.append(i2)
                    for i in new['data']['specialFeatured']['entries']:
                        for i2 in i['items']:
                            try:
                                i2['price'] = i['finalPrice']
                            except KeyError:
                                i2['price'] = 0
                            newitems.append(i2)
                    for temp in newitems:
                        count = 0
                        for temp2 in newitems:
                            if temp['id'] == temp2['id']:
                                count += 1
                                if count >= 2:
                                    newitems.remove(temp2)
                    user, db = await sql.c()
                    for i in newitems:
                        try:
                            await db.execute("SELECT * FROM remindlist WHERE itemid=%s", (i['id'],))
                            anschreiben = await db.fetchall()
                            for useranschreiben in anschreiben:
                                tuser = self.client.get_user(useranschreiben[0])
                                embed = discord.Embed(color=SETTINGS.embedcolor,
                                                      description=f"An item from your remind "
                                                                  f"list is in the Item Shop!\n\n"
                                                                  f"> **Item:** {i['name']} ({i['type']['displayValue']})\n"
                                                                  f"> **Price:** {i['price']} <:vbucks:757663520467845130>")
                                embed.set_footer(
                                    text=f"We would be happy if you would use the Creator Code \"AcNono_\"",
                                    icon_url="https://cdn.discordapp.com/emojis/757664893980901497.png")
                                try:
                                    embed.set_thumbnail(url=i['images']['icon'])
                                except:
                                    try:
                                        embed.set_thumbnail(url=i['images']['smallIcon'])
                                    except:
                                        pass
                                await tuser.send(embed=embed)
                        except:
                            traceback.print_exc()
                            continue
                    await user.commit()
                    await db.close()

            except:
                traceback.print_exc()
                await (await aiofiles.open('Cache/shopdata.json', mode='w+')).write(
                    json.dumps(new, indent=2))

    @commands.command()
    @commands.is_owner()
    async def deletelastshop(self, ctx):
        user, db = await sql.c()
        await db.execute("SELECT * FROM lastshop")
        data = await db.fetchall()
        await db.execute("DELETE FROM lastshop")
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

    @commands.group()
    async def shopreminder(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                color=SETTINGS.embedcolor,
                title="Shop Reminder",
                description="**Subcommands:**\n"
                            "``>shopreminder add`` - Add a Item to the your reminder list\n "
                            "``>shopreminder remove`` - Delete a Item from your reminder list\n"
                            "``>shopreminder list`` - Display all Items from your reminder list\n")
            embed.set_footer(text=f"Note: Please enable your DM's")
            return await ctx.send(embed=embed)

    @shopreminder.command()
    async def add(self, ctx, *, name: str = None):
        if name is None:
            return await ctx.send(embed=discord.Embed(color=SETTINGS.embedcolor, description=f"Please add a Name."))
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://fortnite-api.com/v2/cosmetics/br/search?name={name}&matchMethod=contains") as resp:
                if resp.status == 404:
                    try:
                        return await ctx.send(
                            embed=discord.Embed(color=SETTINGS.embedcolor, title="Item cannot be found",
                                                description=f"{(await resp.json())['error']}"))
                    except:
                        return await ctx.send(
                            embed=discord.Embed(color=SETTINGS.embedcolor, title="Item cannot be found"))
                else:
                    data = (await resp.json())['data']
                    user, db = await sql.c()
                    await db.execute("SELECT * FROM remindlist WHERE id=%s and itemid=%s", (ctx.author.id, data['id'],))
                    id = await db.fetchone()
                    if id:
                        await db.close()
                        user.close()
                        return await ctx.send(
                            embed=discord.Embed(color=SETTINGS.embedcolor,
                                                title="This Item is already on your remind list"))
                    embed = discord.Embed(color=SETTINGS.embedsuccess,
                                          title="Item added",
                                          description=f"The Item ``{data['name']}`` was added to your remind list.")
                    embed.set_footer(text=f"Note: Please enable your DM's")
                    try:
                        embed.set_thumbnail(url=data['images']['icon'])
                    except:
                        try:
                            embed.set_thumbnail(url=data['images']['smallIcon'])
                        except:
                            pass
                    await ctx.send(f"{ctx.author.mention}", embed=embed)

                    await db.execute("INSERT INTO remindlist VALUE (%s, %s)", (ctx.author.id, data['id'],))
                    await user.commit()
                    await db.close()
                    user.close()

    @shopreminder.command()
    async def remove(self, ctx, *, name: str = None):
        if name is None:
            return await ctx.send(embed=discord.Embed(color=SETTINGS.embedcolor, description=f"Please add a Name."))
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://fortnite-api.com/v2/cosmetics/br/search?name={name}&matchMethod=contains") as resp:
                if resp.status == 404:
                    try:
                        return await ctx.send(
                            embed=discord.Embed(color=SETTINGS.embedcolor, title="Item cannot be found",
                                                description=f"{(await resp.json())['error']}"))
                    except:
                        return await ctx.send(
                            embed=discord.Embed(color=SETTINGS.embedcolor, title="Item cannot be found"))
                else:
                    data = (await resp.json())['data']
                    user, db = await sql.c()
                    await db.execute("SELECT * FROM remindlist WHERE id=%s and itemid=%s", (ctx.author.id, data['id'],))
                    id = await db.fetchone()
                    if not id:
                        return await ctx.send(
                            embed=discord.Embed(color=SETTINGS.embedcolor,
                                                title="This Item is not on your remind list"))
                    embed = discord.Embed(color=SETTINGS.embederror,
                                          title="Item removed",
                                          description=f"The Item ``{data['name']}`` was removed to your remind list.")
                    try:
                        embed.set_thumbnail(url=data['images']['icon'])
                    except:
                        try:
                            embed.set_thumbnail(url=data['images']['smallIcon'])
                        except:
                            pass
                    await ctx.send(f"{ctx.author.mention}", embed=embed)
                    await db.execute("DELETE FROM remindlist WHERE id=%s and itemid=%s", (ctx.author.id, data['id'],))
                    await user.commit()
                    await db.close()
                    user.close()

    @shopreminder.command()
    async def list(self, ctx):
        user, db = await sql.c()
        await db.execute("SELECT * FROM remindlist WHERE id=%s", (ctx.author.id,))
        id = await db.fetchall()
        if not id:
            return await ctx.send(
                embed=discord.Embed(color=SETTINGS.embedcolor,
                                    title="You dont have Items on your remind list"))
        tempstring = "These Items are on your remind list:\n\n"
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://fortnite-api.com/v2/cosmetics/br') as data:
                data = await data.json()
        for i in id:
            for i2 in data['data']:
                if i[1] == i2['id']:
                    tempstring += f"- {i2['name']}\n"
        await db.close()
        user.close()
        await modules.paginator.TextPages(ctx=ctx, text=tempstring).paginate()

    def cog_unload(self):
        self.checkstore.stop()
        self.fortniteapiupdate.stop()
        print("shop LOOP BEENDET")
        try:
            self.client.unload_extension("cogs.shop")
            self.client.load_extension("cogs.shop")
        except:
            self.client.load_extension("cogs.shop")
            print("CANOT RELOAD EXTENSION shop")


def setup(client):
    client.add_cog(shop(client))
