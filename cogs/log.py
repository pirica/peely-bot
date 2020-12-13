import asyncio
import datetime

import discord
import pytz
from discord.ext import commands, tasks

from Settings import SETTINGS
from modules import sql


def td_format(seconds):
    periods = [('year', 60 * 60 * 24 * 365), ('month', 60 * 60 * 24 * 30), ('day', 60 * 60 * 24), ('hour', 60 * 60),
               ('minute', 60), ('second', 1)]
    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))
    return ", ".join(strings)


class log(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logcache = {}

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.cache.start()
        except Exception as ex:
            print(ex)
            await self.cache.stop()
            await asyncio.sleep(1)
            await self.cache.start()

    @tasks.loop(seconds=45)
    async def cache(self):
        user, db = await sql.c()
        await db.execute("SELECT * FROM logging")
        data = await db.fetchall()
        for i in data:
            self.logcache[str(i[0])] = str(i[1])
        await db.close()
        user.close()

    async def getlogchannel(self, guildid):
        getg = self.logcache.get(str(guildid))
        if getg:
            return int(getg)
        else:
            return None

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        data = await self.getlogchannel(channel.guild.id)
        if data:
            mchannel = self.client.get_channel(data)
            embed = discord.Embed(color=SETTINGS.embederror)
            embed.set_author(name=f"Deleted Channel")
            embed.add_field(name=f"Channel:", value=channel.name)
            await mchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        data = await self.getlogchannel(channel.guild.id)
        if data:
            mchannel = self.client.get_channel(data)
            embed = discord.Embed(color=SETTINGS.embedsuccess)
            embed.set_author(name=f"New Channel")
            embed.add_field(name=f"Channel:", value=channel.name)
            await mchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        data = await self.getlogchannel(role.guild.id)
        if data:
            mchannel = self.client.get_channel(data)
            embed = discord.Embed(color=SETTINGS.embederror)
            embed.set_author(name=f"Deleted Role")
            embed.add_field(name=f"Role:", value=role.name)
            try:
                await mchannel.send(embed=embed)
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        data = await self.getlogchannel(role.guild.id)
        if data:
            mchannel = self.client.get_channel(data)
            embed = discord.Embed(color=SETTINGS.embedsuccess)
            embed.set_author(name=f"New Role")
            embed.add_field(name=f"Role:", value=role.name)
            await mchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = await self.getlogchannel(member.guild.id)
        if data:
            mchannel = self.client.get_channel(data)
            embed = discord.Embed(color=SETTINGS.embedsuccess)
            embed.set_author(name=f"A User joined your Server")
            embed.add_field(name=f"Name:", value=member.display_name)
            embed.add_field(name=f"Created at:", value=member.created_at.__format__('%A, %B %d, %Y'))
            await mchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        data = await self.getlogchannel(guild.id)
        if data:
            mchannel = self.client.get_channel(data)
            embed = discord.Embed(color=SETTINGS.embederror)
            embed.set_author(name=f"A Member was banned from the Server")
            embed.add_field(name=f"Name:", value=member.display_name)
            embed.add_field(name=f"Created at:", value=member.created_at.__format__('%A, %B %d, %Y'))
            try:
                embed.add_field(name=f"Joined at:", value=member.joined_at.__format__('%A, %B %d, %Y'))
            except:
                pass
            await mchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        data = await self.getlogchannel(guild.id)
        if data:
            mchannel = self.client.get_channel(data)
            embed = discord.Embed(color=SETTINGS.embedsuccess)
            embed.set_author(name=f"A Member was unbanned from the Server")
            embed.add_field(name=f"Name:", value=member.name)
            embed.add_field(name=f"Created at:", value=member.created_at.__format__('%A, %B %d, %Y'))
            await mchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        data = await self.getlogchannel(member.guild.id)
        if data:
            mchannel = self.client.get_channel(data)
            embed = discord.Embed(color=SETTINGS.embederror)
            embed.set_author(name=f"A User left your Server")
            embed.add_field(name=f"Name:", value=member.display_name)
            embed.add_field(name=f"Created at:", value=member.created_at.__format__('%A, %B %d, %Y'))
            embed.add_field(name="Time stayed on server",
                            value=td_format(int((datetime.datetime.utcnow() - member.joined_at).total_seconds())))
            await mchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        data = await self.getlogchannel(after.guild.id)
        if data:
            mchannel = self.client.get_channel(data)
            if before.display_name != after.display_name:
                embed = discord.Embed(color=SETTINGS.embedsuccess,
                                      description=f":pencil: {after.mention} **nickname edited**")
                embed.set_author(name=f"{after.name}#{after.discriminator}", icon_url=after.avatar_url)
                embed.add_field(name=f"**Old Nickname**", value=f"``{before.display_name}``")
                embed.add_field(name=f"**New Nickname**", value=f"``{after.display_name}``")
                embed.timestamp = datetime.datetime.now(tz=pytz.timezone("Europe/Berlin"))
                await mchannel.send(embed=embed)
            if before.roles != after.roles:
                if len(before.roles) < len(after.roles):
                    for role in after.roles:
                        if role not in before.roles:
                            embed = discord.Embed(color=SETTINGS.embedsuccess,
                                                  description=f":white_check_mark: {after.mention} **role added**")
                            embed.set_author(name=f"{after.name}#{after.discriminator}", icon_url=after.avatar_url)
                            embed.add_field(name=f"**New Role**", value=role.mention)
                            embed.timestamp = datetime.datetime.now(tz=pytz.timezone("Europe/Berlin"))
                            await mchannel.send(embed=embed)
                if len(before.roles) > len(after.roles):
                    for role in before.roles:
                        if role not in after.roles:
                            embed = discord.Embed(color=SETTINGS.embederror,
                                                  description=f"⛔️ {after.mention} **role removed**")
                            embed.set_author(name=f"{after.name}#{after.discriminator}", icon_url=after.avatar_url)
                            embed.add_field(name=f"**Role removed**", value=role.mention)
                            embed.timestamp = datetime.datetime.now(tz=pytz.timezone("Europe/Berlin"))
                            await mchannel.send(embed=embed)

            if before.avatar_url != after.avatar_url:
                embed = discord.Embed(color=SETTINGS.embedsuccess,
                                      description=f":pencil: {after.mention} **new avatar**")
                embed.set_author(name=f"{after.name}#{after.discriminator}", icon_url=after.avatar_url)
                embed.set_image(url=after.avatar_url)
                embed.timestamp = datetime.datetime.now(tz=pytz.timezone("Europe/Berlin"))
                await mchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        data = await self.getlogchannel(message.guild.id)
        if data:
            channel = self.client.get_channel(data)
            if message.embeds:
                return
            user2 = self.client.get_user(message.author.id)
            if user2.bot is True:
                return
            embed = discord.Embed(color=SETTINGS.embederror)
            embed.set_author(name=f"Deleted Message | Sent by {message.author.display_name}",
                             icon_url=message.author.avatar_url)
            embed.add_field(name=f"Message:", value=message.content)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, message):
        if before == message:
            return
        if before.content == message.content:
            return
        data = await self.getlogchannel(message.guild.id)
        if data:
            channel = self.client.get_channel(data)
            if message.embeds:
                return
            user2 = self.client.get_user(message.author.id)
            if user2.bot is True:
                return
            embed = discord.Embed(color=SETTINGS.embederror)
            embed.set_author(name=f"Edited Message | Sent by {message.author.display_name}",
                             icon_url=message.author.avatar_url)
            embed.add_field(name=f"Before:", value=before.content)
            embed.add_field(name=f"After:", value=message.content)
            await channel.send(embed=embed)


def setup(client):
    client.add_cog(log(client))
