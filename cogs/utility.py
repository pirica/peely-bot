import asyncio
import copy
import io
import os
import random
import subprocess
import sys
import textwrap
import traceback
from contextlib import redirect_stdout
from datetime import datetime
from typing import Optional

import aiohttp
import discord
import psutil
from discord.ext import commands

from Settings import SETTINGS
from modules import sql, paginator


async def get_status(client):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://ft308v428dv3.statuspage.io/api/v2/components.json') as data:
            Status = await data.json()
    NewStatus = {}
    for i in Status["components"]:
        # Website
        if i["id"] == "l483xcldq6qk":
            Website = i["status"]
            NewStatus["Website"] = i["status"]
        # Game Services
        if i["id"] == "t9xpn32q9jlb":
            GameServices = i["status"]
            NewStatus["Game Services"] = i["status"]
        # Login
        if i["id"] == "gp7pb08zbsm1":
            Login = i["status"]
            NewStatus["Login"] = i["status"]
        # Parties, Friends, and Messaging
        if i["id"] == "h591868l4p8r":
            Parties_Friends_and_Messaging = i["status"]
            NewStatus["Parties, Friends, and Messaging"] = i["status"]
        # Voice Chat
        if i["id"] == "12xt5b2ysxtk":
            VoiceChat = i["status"]
            NewStatus["Voice Chat"] = i["status"]
        # Matchmaking
        if i["id"] == "n62jd9mnxgnf":
            Matchmaking = i["status"]
            NewStatus["Matchmaking"] = i["status"]
        # Stats and Leaderboards
        if i["id"] == "x6np52ybtwrv":
            Stats_and_Leaderboards = i["status"]
            NewStatus["Stats and Leaderboards"] = i["status"]
        # Item Shop
        if i["id"] == "689s95gldrs3":
            ItemShop = i["status"]
            NewStatus["Item Shop"] = i["status"]
    counter = 0
    for i23 in NewStatus:
        if NewStatus[i23] == "operational":
            counter += 1
    if counter > 7:
        embed = discord.Embed(color=0x00FF00)
    else:
        embed = discord.Embed(color=0xFF0000)
    for i2 in NewStatus:
        if NewStatus[i2] == "operational":
            emoji = "✅"
        else:
            emoji = "❌"
        embed.set_author(name=f"Fortnite Server Status", url="https://status.epicgames.com",
                         icon_url="https://cdn.discordapp.com/icons/322850917248663552/096863ef3b1463545e4e4fe71882e6b3.png?size=2048")
        nono = client.get_user(SETTINGS.nono)
        embed.set_footer(text=f"Made by {nono.name}#{nono.discriminator}", icon_url=nono.avatar_url)
        embed.add_field(value=f"{emoji} **-** {NewStatus[i2]}", name=f"{i2}", inline=False)
    return embed


class GlobalChannel(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return await commands.TextChannelConverter().convert(ctx, argument)
        except commands.BadArgument:
            # Not found... so fall back to ID + global lookup
            try:
                channel_id = int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f'Could not find a channel by ID {argument!r}.')
            else:
                channel = ctx.bot.get_channel(channel_id)
                if channel is None:
                    raise commands.BadArgument(f'Could not find a channel by ID {argument!r}.')
                return channel


def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')


class utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=False, usage="Get the current Status")
    async def status(self, ctx):
        msg = await ctx.send(embed=discord.Embed(description=f"Loading", color=SETTINGS.embedcolor))
        await msg.edit(embed=await get_status(client=self.client))

    @commands.command(hidden=True, usage=f"Restart everything. [ONLY MY OWNER CAN DO THAT]")
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.send("Bye Bye")
        await asyncio.sleep(3)
        sys.exit(1)

    @commands.command(usage=f"The invite link for the Support Server")
    async def support(self, ctx):
        try:
            await ctx.author.send("https://discord.gg/fX8b8Wh")
            await ctx.send("Please check your DM's!")
        except:
            await ctx.send("https://discord.gg/fX8b8Wh")

    @commands.command(usage=f"The invite link for the Bot")
    async def invite(self, ctx):
        await ctx.send("https://peely.de/invite")

    @commands.command(usage="The the Stats of the Bot", aliases=["botinfo", "botstats"])
    async def botstatus(self, ctx):
        message = await ctx.send(f"Loading Stats for the Bot.")
        embed = discord.Embed(color=SETTINGS.embedsuccess)
        embed.set_author(name=f"Stats for {self.client.user.name}", icon_url=self.client.user.avatar_url)
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        process = psutil.Process(os.getpid())
        ram = process.memory_info().rss
        ram = int(ram) / 1024 / 1024
        ram = ram.__round__(2)
        embed.add_field(name="Ram", value=str(ram) + "mb")
        embed.add_field(name=f"Uptime:", value=f"{days}d, {hours}h, {minutes}m, {seconds}s")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://discord.statuspage.io/metrics-display/ztt4777v23lf/day.json') as data:
                ping = await data.json()
        ping = int(ping["summary"]["last"])
        embed.add_field(name=f"Discord API Ping:", value=f"{ping}ms")
        extremec = 0
        highc = 0
        lowc = 0
        mediumc = 0
        nonec = 0
        guildc = 0
        txtc = 0
        voic = 0
        cc = 0
        boosttotalc = 0
        totaluser = 0
        lev1c = 0
        lev2c = 0
        lev3c = 0
        offline = 0
        dnd = 0
        afk = 0
        online = 0
        invisible = 0
        for i in self.client.guilds:
            guildc += 1
            for txt in i.text_channels:
                txtc += 1
            for voice in i.voice_channels:
                voic += 1
            for cccccc in i.categories:
                cc += 1
            if i.premium_tier == 1:
                lev1c += 1
            if i.premium_tier == 2:
                lev2c += 1
            if i.premium_tier == 3:
                lev3c += 1
            boosttotalc += i.premium_subscription_count

            if str(i.verification_level) == "none":
                nonec += 1
            elif str(i.verification_level) == "low":
                lowc += 1
            elif str(i.verification_level) == "medium":
                mediumc += 1
            elif str(i.verification_level) == "high":
                highc += 1
            elif str(i.verification_level) == "extreme":
                extremec += 1
            for i2 in i.members:
                if str(i2.status) == "online":
                    online += 1
                elif str(i2.status) == "offline":
                    offline += 1
                elif str(i2.status) == "idle":
                    afk += 1
                elif str(i2.status) == "dnd":
                    dnd += 1
                elif str(i2.status) == "invisible":
                    invisible += 1
                totaluser += 1
        embed.add_field(name=f"Server Verification:", value=f"{extremec} - Extreme\n"
                                                            f"{highc} - High\n"
                                                            f"{lowc} - Low\n"
                                                            f"{mediumc} - Medium\n"
                                                            f"{nonec} - None")
        embed.add_field(name=f"Counters:", value=f"Server: {guildc}\n"
                                                 f"Text Channels: {txtc}\n"
                                                 f"Voice Channels: {voic}\n"
                                                 f"Categories: {cc}\n"
                                                 f"Users: {totaluser}\n"
                                                 f"User online: {online}\n"
                                                 f"User Do Not Disturb: {dnd}\n"
                                                 f"User afk: {afk}\n"
                                                 f"User offline: {offline}\n")
        embed.add_field(name=f"Nitro boosts:",
                        value=f"Total: {boosttotalc}\n:one: Level: {lev1c}\n:two: Level: {lev2c}\n:three: Level: {lev3c}")
        await message.edit(content=None, embed=embed)

    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.is_owner()
    async def eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'client': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    async def run_process(self, command):
        try:
            process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await process.communicate()
        except NotImplementedError:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await self.client.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sudo(self, ctx, channel: Optional[GlobalChannel], who: discord.User, *, command: str):
        """Run a command as another user optionally in another channel."""
        msg = copy.copy(ctx.message)
        channel = channel or ctx.channel
        msg.channel = channel
        msg.author = channel.guild.get_member(who.id) or who
        msg.content = ctx.prefix + command
        new_ctx = await self.client.get_context(msg, cls=type(ctx))
        await self.client.invoke(new_ctx)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sh(self, ctx, *, command):
        """Runs a shell command."""

        async with ctx.typing():
            stdout, stderr = await self.run_process(command)

        if stderr:
            text = f'stdout:\n{stdout}\nstderr:\n{stderr}'
        else:
            text = stdout

        try:
            await paginator.TextPages(ctx=ctx, text=text).paginate()
        except Exception as e:
            await ctx.send(str(e))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for i in guild.members:
            if i.guild_permissions.administrator or i.guild_permissions.manage_guild:
                embed = discord.Embed(color=SETTINGS.embedsuccess)
                embed.set_author(name=f"Thank you for adding {self.client.user.name} to {guild.name}")
                embed.add_field(name=f"Please setup the Bot:",
                                value=f"Visit our [Webdashboard](https://peely.de/login).\nIf you need help, you can watch the [YouTube Tutorial](https://www.youtube.com/watch?v=dP-0wxNHqzM).\nYou can also check out our [Documentation](https://docs.peely.de/)")
                try:
                    await i.send(embed=embed)
                except:
                    continue

    @commands.command(usage="Get the Time when you or a mentioned person joined the Server")
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        await ctx.send(f'{member.display_name} joined on {member.joined_at}')

    @commands.command(name='top_role', aliases=['toprole'],
                      usage="Get the Highest role from your or a mentioned person")
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')

    @commands.command()
    async def map(self, ctx):
        embed = discord.Embed(color=SETTINGS.embedsuccess, title=f"Fortnite-Map")
        embed.set_image(url="https://fortnite-api.com/images/br/map.png")
        await ctx.send(embed=embed)

    @commands.command(name='perms', aliases=['perms_for', 'permissions'],
                      usage="Show all permissions for a user or your own.")
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member = None):

        if not member:
            member = ctx.author

        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)

    @commands.command(usage="Create a Custom URL. (URL Shoorter)")
    async def customurl(self, ctx, url: str = None, customurl: str = None):
        if not url:
            return await ctx.send(embed=discord.Embed(
                description=f"Please use the command like that: ``>customurl <https://peely.de/> [customurl]``",
                color=SETTINGS.embederror))
        try:
            temp = await sql.c()
            user = temp[0]
            db = temp[1]
            await db.execute("SELECT * FROM urlshorter WHERE shorturl=%s", (customurl,))
            data = await db.fetchall()
            if data:
                while True:
                    buchstaben = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                                  "r",
                                  "s",
                                  "t", "u", "v", "w", "x", "y", "z", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    code = ""
                    for i in range(6):
                        dasint = random.randint(0, 35)
                        code += f"{buchstaben[dasint]}"
                    temp = await sql.c()
                    user = temp[0]
                    db = temp[1]
                    await db.execute("SELECT * FROM urlshorter WHERE shorturl=%s", (code,))
                    data = await db.fetchall()
                    if data:
                        continue
                    else:
                        await db.execute("INSERT INTO urlshorter VALUE (%s, %s)", (url, code,))
                        await user.commit()
                    await db.close()
                    user.close()
                    return await ctx.send(
                        f"This custom url already exists. Therefore, it has now been generated randomly. The URL can be reached at https://peely.de/url/{code}")

            else:
                await db.execute("INSERT INTO urlshorter VALUE (%s, %s)", (url, customurl,))
            await user.commit()
            await db.close()
            user.close()
            return await ctx.send(f"Successful. The URL can be reached at https://peely.de/url/{customurl}")

        except Exception as ex:
            print(ex)
            while True:
                buchstaben = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                              "s",
                              "t", "u", "v", "w", "x", "y", "z", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                code = ""
                for i in range(6):
                    dasint = random.randint(0, 35)
                    code += f"{buchstaben[dasint]}"
                user, db = await sql.c()
                await db.execute("SELECT * FROM urlshorter WHERE shorturl=%s", (code,))
                data = await db.fetchall()
                if data:
                    continue
                else:
                    await db.execute("INSERT INTO urlshorter VALUE (%s, %s)", (url, code,))
                    await user.commit()
                user.close()
                await db.close()
                return await ctx.send(f"Successful. The URL can be reached at https://peely.de/url/{code}")

    @commands.command(hidden=True, usage="Create Patch Notes [ONLY MY PROGRAMMER CAN DO THAT]")
    @commands.is_owner()
    async def createpatch(self, ctx, *, text: str):
        channel = self.client.get_channel(706400633091129415)
        embed = discord.Embed(color=SETTINGS.embedsuccess, description=text)
        embed.set_author(icon_url=self.client.user.avatar_url, url=f"https://peely.de", name=f"Patch Notes")
        embed.set_footer(text="React on the Emoji to get pinged on Patch Notes/News/and Polls.")
        msg = await channel.send("<@&706400632994529315>", embed=embed)
        await msg.add_reaction("✔️")

    @commands.command(hidden=True, usage="Send a Text to all Leak channels")
    @commands.is_owner()
    async def sendtexttoleaks(self, ctx, *, text: str):
        temp = await sql.c()
        user = temp[0]
        db = temp[1]
        await db.execute("SELECT * from leaks")
        data = await db.fetchall()
        await db.close()
        user.close()
        nono = self.client.get_user(SETTINGS.nono)
        for i in data:
            channel = self.client.get_channel(i[1])
            if not channel:
                continue
            embed = discord.Embed(color=SETTINGS.embederror, description=text)
            embed.set_author(icon_url=nono.avatar_url, url=f"https://peely.de",
                             name=f"News from the {self.client.user.name} Bot.")
            try:
                await channel.send(embed=embed)
            except:
                pass

    @commands.command(hidden=True, usage="Send a Text to all News channels")
    @commands.is_owner()
    async def sendtexttonews(self, ctx, *, text: str):
        temp = await sql.c()
        user = temp[0]
        db = temp[1]
        await db.execute("SELECT * from news")
        data = await db.fetchall()
        await db.close()
        user.close()
        nono = self.client.get_user(SETTINGS.nono)
        for i in data:
            channel = self.client.get_channel(i[1])
            if not channel:
                continue
            embed = discord.Embed(color=SETTINGS.embederror, description=text)
            embed.set_author(icon_url=nono.avatar_url, url=f"https://peely.de",
                             name=f"News from the {self.client.user.name} Bot.")
            try:
                await channel.send(embed=embed)
            except:
                pass

    @commands.command(hidden=True, usage="Send a Text to all shop channels")
    @commands.is_owner()
    async def sendtexttoshop(self, ctx, *, text: str):
        temp = await sql.c()
        user = temp[0]
        db = temp[1]
        await db.execute("SELECT * from shop")
        data = await db.fetchall()
        await db.close()
        user.close()
        nono = self.client.get_user(SETTINGS.nono)
        for i in data:
            channel = self.client.get_channel(i[1])
            if not channel:
                continue
            embed = discord.Embed(color=SETTINGS.embederror, description=text)
            embed.set_author(icon_url=nono.avatar_url, url=f"https://peely.de",
                             name=f"News from the {self.client.user.name} Bot.")
            try:
                await channel.send(embed=embed)
            except:
                pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id in [706400633091129415, 706400633091129417, 706400633091129416]:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(706400632994529315)
            try:
                await member.add_roles(role)
            except:
                pass


def setup(client):
    client.add_cog(utility(client))
