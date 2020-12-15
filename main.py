import asyncio
import json
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

import aiohttp
import discord
import psutil
import pytz
from discord.ext import commands, tasks

import SECRETS
from Settings import SETTINGS
from modules import sql, permissions

cachedprefix = {}


def get_prefix(client, message):
    if not message.guild:
        return ">"
    if cachedprefix.get(str(message.guild.id)):
        return str(cachedprefix.get(str(message.guild.id)))
    return ">"


intents = discord.Intents.all()

client = commands.Bot(command_prefix=get_prefix, activity=discord.Game(">help | https://peely.de"), intents=intents)
client.remove_command("help")
client.launch_time = datetime.utcnow()


def check(ctx):
    return permissions.check(ctx)


###############################################################################################


@client.event
async def on_ready():
    print("Discord Client geladen")
    print(client.user.name)
    await sql.sqlsetup()
    try:
        await check2.start()
    except Exception as ex:
        print(ex)
        await check2.stop()
        await asyncio.sleep(1)
        await check2.start()
    try:
        await post.start()
    except Exception as ex:
        print(ex)
        await post.stop()
        await asyncio.sleep(1)
        await post.start()
    try:
        await cache.start()
    except Exception as ex:
        print(ex)
        await cache.stop()
        await asyncio.sleep(1)
        await cache.start()


for file in Path('cogs').glob('**/*.py'):
    *tree, _ = file.parts
    try:
        client.load_extension(f"{'.'.join(tree)}.{file.stem}")
        print(f"{'.'.join(tree)}.{file.stem} loaded")
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


@client.command(name='load', hidden=True)
async def cog_load(ctx, *, cog: str):
    if ctx.author.id != 640235175007223814:
        return
    try:
        client.load_extension("cogs." + cog)
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')


@client.command(name='unload', hidden=True)
async def cog_unload(ctx, *, cog: str):
    if ctx.author.id != 640235175007223814:
        return
    try:
        client.unload_extension("cogs." + cog)
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')


@client.command(name='reload', hidden=True)
async def cog_reload(ctx, *, cog: str):
    if ctx.author.id != 640235175007223814:
        return
    try:
        client.unload_extension("cogs." + cog)
        await asyncio.sleep(0.5)
        client.load_extension("cogs." + cog)
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')


# Commands
@client.command(usage=f">help [Command]", aliases=["commands", "hilfe", "setup", "config", "configure"])
async def help(ctx, *, cog: str = None):
    user, db = await sql.c()
    await db.execute("SELECT * FROM prefix WHERE guild=%s", (ctx.guild.id,))
    data = await db.fetchone()
    await db.close()
    user.close()
    prefix = ">"
    if data:
        prefix = str(data[1])
    try:
        if not cog:
            embed = discord.Embed(color=SETTINGS.embedsuccess)
            embed.set_author(name=f"Help for Peely", url="https://peely.de", icon_url=client.user.avatar_url)
            string = ""
            for cog in client.cogs:
                if str(cog) == "logging":
                    continue
                if str(cog) == "leaks":
                    continue
                if str(cog) == "status":
                    continue
                if str(cog) == "footer":
                    continue
                if str(cog) == "shop":
                    continue
                if str(cog) == "dailyrestart":
                    continue
                if str(cog) == "cosmetics":
                    continue
                if str(cog) == "tournaments":
                    continue
                if str(cog) == "footer":
                    continue
                string += f"{prefix}help {cog}\n"
            string += f"{prefix}help customgames"
            embed.add_field(name=f"Help for the Systems:", value=f"``{string}``", inline=False)
            newstring = ""
            user, db = await sql.c()
            await db.execute("SELECT * FROM customcommand WHERE guild=%s", (ctx.guild.id,))
            data = await db.fetchall()
            await db.close()
            user.close()
            if data:
                for i in data:
                    newstring += f"{prefix}{i[1]}\n"
                embed.add_field(name=f"Commands for this Server", value=newstring, inline=False)

            if ctx.guild.id != 706400632994529310:
                embed.add_field(name="Do you need more Help?",
                                value=f"Join our [Support Server](https://discord.gg/fX8b8Wh)\nDont you know how to setup the Bot? Visit our ["
                                      f"Webdashboard](https://peely.de/login)", inline=False)
            else:
                embed.add_field(name="Do you need more Help?",
                                value=f"Dont you know how to setup the Bot? Visit our ["
                                      f"Webdashboard](https://peely.de/login)", inline=False)
            embed.add_field(name=f"Do you want to Invite the Bot?",
                            value=f"Visit our Website at https://peely.de/invite", inline=False)
            await ctx.send(embed=embed)
        else:
            if cog.lower() == "customgames":
                embed = discord.Embed(color=SETTINGS.embedsuccess)
                embed.add_field(name=f"All commands in the {cog} System",
                                value=f"{prefix}createcustom | Create a Custom Games Match\n\nNeed to configure at "
                                      f"the Dashboard",
                                inline=False)
                if ctx.guild.id != 706400632994529310:
                    embed.add_field(name="Do you need more Help?",
                                    value=f"Join our [Support Server](https://discord.gg/fX8b8Wh)\nDont you know how "
                                          f"to setup the Bot? Visit our [ "
                                          f"Webdashboard](https://peely.de/login) and our [Documentation]("
                                          f"https://docs.peely.de).",
                                    inline=False)
                else:
                    embed.add_field(name="Do you need more Help?",
                                    value=f"Dont you know how to setup the Bot? Visit our ["
                                          f"Webdashboard](https://peely.de/login) and our [Documentation]("
                                          f"https://docs.peely.de).",
                                    inline=False)
                embed.add_field(name=f"Do you want to Invite the Bot?",
                                value=f"Visit our Website at https://peely.de/invite", inline=False)
                await ctx.send(embed=embed)
            coginstance = client.get_cog(cog.lower())
            if coginstance is None:
                return await ctx.send(
                    embed=discord.Embed(
                        color=SETTINGS.embederror,
                        title="System not found",
                        description=f"The Help command has been divided into systems for clarity.\n"
                                    f"Please write a system name from the list above after the help command."))
            else:
                commands = coginstance.get_commands()
                newstring = ""
                for command in commands:
                    if command.name == "restart":
                        continue
                    if command.name == "createpatch":
                        continue
                    if command.name == "createnews":
                        continue
                    if command.name == "admin":
                        continue
                    if command.name == "say":
                        continue
                    if command.name == "deletelastshop":
                        continue
                    if command.name == "deletelastleaks":
                        continue
                    if command.name == "createinvite":
                        continue
                    if command.name == "eval":
                        continue
                    if command.name == "sh":
                        continue
                    if command.name == "sudo":
                        continue
                    if command.name == "sendtexttoshop":
                        continue
                    if command.name == "sendtexttoleaks":
                        continue
                    if command.name == "sendtexttonews":
                        continue
                    if command.name == "loadcachedstore":
                        continue
                    if command.name == "loadcachednews":
                        continue
                    if command.name == "genshop":
                        continue
                    if command.name == "genshopforall":
                        continue
                    if command.name == "cachedstore":
                        continue
                    if command.name == "uptime":
                        continue
                    if command.name == "botstatus":
                        continue
                    if command.name == "cachedstore":
                        continue
                    if command.name == "sendtexttonews ":
                        continue
                    if command.usage is None:
                        command.usage = "Not defind"
                    newstring += f"{prefix}{command.name} - {command.usage}\n"
                embed = discord.Embed(color=SETTINGS.embedsuccess)
                embed.add_field(name=f"All commands in the {cog} System", value=f"{newstring}", inline=False)
                if ctx.guild.id != 706400632994529310:
                    embed.add_field(name="Do you need more Help?",
                                    value=f"Join our [Support Server](https://discord.gg/fX8b8Wh)\nDont you know how to setup the Bot? Visit our ["
                                          f"Webdashboard](https://peely.de/login) and our [Documentation](https://docs.peely.de).",
                                    inline=False)
                else:
                    embed.add_field(name="Do you need more Help?",
                                    value=f"Dont you know how to setup the Bot? Visit our ["
                                          f"Webdashboard](https://peely.de/login) and our [Documentation](https://docs.peely.de).",
                                    inline=False)
                embed.add_field(name=f"Do you want to Invite the Bot?",
                                value=f"Visit our Website at https://peely.de/invite", inline=False)
                await ctx.send(embed=embed)
    except Exception as ex:
        print(ex)


@client.command()
async def createcustom(ctx):
    return


@tasks.loop(hours=1)
async def post():
    if SETTINGS.test is False:
        async with aiohttp.ClientSession() as session:
            parms = {
                "Authorization": SECRETS.botsdatabase,
                "Content-Type": "application/json"
            }
            data = {
                "servers": len(client.user.guilds)
            }
            await session.post(f"https://api.botsdatabase.com/v1/bots/{client.user.id}", headers=parms,
                               data=json.dumps(data))

            parms = {
                "Authorization": SECRETS.botlistspace,
                "Content-Type": "application/json"
            }
            data = {
                "servers": len(client.user.guilds)
            }
            await session.post(f"https://api.botlist.space/"
                               f"v1/bots/{client.user.id}", headers=parms,
                               data=json.dumps(data))

            parms = {
                "Authorization": SECRETS.discordboats,
            }
            data = {
                "server_count": len(client.user.guilds)
            }
            await session.post(f"https://discord.boats/api"
                               "/bot/{client.user.id}", headers=parms,
                               data=json.dumps(data))


@tasks.loop(seconds=45)
async def cache():
    user, db = await sql.c()
    await db.execute("SELECT * FROM prefix")
    data = await db.fetchall()
    for i in data:
        cachedprefix[str(i[0])] = str(i[1])
    await db.close()
    user.close()


@client.command(aliases=["update", "updatecogs"])
@commands.check(check)
async def reloadall(ctx):
    embed = discord.Embed(title=f"__cog System__", description=f"**I refreshed the following cogs:**", color=0x1df221)
    errors = []
    try:
        for cog in os.listdir('./cogs'):
            if cog.endswith(".py"):
                client.reload_extension(f"cogs.{cog[:-3]}")
                embed.add_field(name=f"``{cog}``", value=f"--------")
    except Exception as ex:
        print(ex)
        errors.append(ex)
    if errors:
        str = ""
        for i in errors:
            str += f"{i}\n"
        await embed.add_field(name=f"Errors:", value=f"{str}")
    await ctx.send(embed=embed, delete_after=15)


@client.command()
@commands.check(check)
async def cogs(ctx):
    embed = discord.Embed(title=f"Cog System", description=f"Cogs:")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            embed.add_field(name=f"``{filename}``", value="--------------", inline=False)
    await ctx.send(embed=embed)


@tasks.loop(minutes=2)
async def check2():
    if SETTINGS.test is True:
        return
    await client.wait_until_ready()
    embed = discord.Embed(color=SETTINGS.embedcolor)
    embed.set_author(name=f"{client.user.name} Status.", icon_url=client.user.avatar_url,
                     url=f"https://peely.de/")
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://discord.statuspage.io/metrics-display/ztt4777v23lf/day.json') as data:
                ping = await data.json()
        ping = int(ping["summary"]["last"])
        embed.add_field(name="Ping of the Discord API", value=str(ping) + "ms", inline=False)
    except:
        embed.add_field(name=f"Ping of the Discord API", value=f"Error", inline=False)
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://peely.de') as peely:
                if peely.status == 200:
                    embed.add_field(name="Website:", value=f"Optimal", inline=False)
                else:
                    embed.add_field(name="Website:", value=f"Error | {peely.status}", inline=False)
    except:
        embed.add_field(name="Website:", value=f"Error | Cannot get the Status.", inline=False)
    process = psutil.Process(os.getpid())
    ram = process.memory_info().rss
    ram = int(ram) / 1024 / 1024
    ram = ram.__round__(2)
    embed.add_field(name="Ram usage:", value=str(ram) + "mb", inline=False)
    embed.set_thumbnail(url="https://img.shields.io/static/"
                            "v1.svg?label=uptime&message=100%25&color=yellow&style=flat")
    embed.set_image(url="https://img.shields.io/static/"
                        "v1.svg?label=status&message=online&color=yellow&style=flat")
    embed.set_footer(text=f"Last Update")
    time2 = datetime.now(tz=pytz.timezone("Europe/Berlin"))
    embed.timestamp = time2
    channel = client.get_channel(712252621125320774)
    msg = await channel.fetch_message(736577786877050911)
    try:
        await msg.edit(embed=embed)
    except:
        pass


loop = asyncio.get_event_loop()
loop.create_task(client.start(SETTINGS.TOKEN, bot=True))
try:
    loop.run_forever()
except:
    pass
finally:
    loop.stop()
