import datetime

import discord
from discord.ext import commands

from Settings import SETTINGS
from modules import sql


class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["setwelcome", "setwelcomechannel"], usage="Set a Welcome Channel for your Server.")
    async def set_welcome(self, ctx, channel: discord.TextChannel = None):
        if ctx.message.author.guild_permissions.administrator:
            if channel is None:
                return await ctx.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                          description=f"You need to add an Channel. ```>set_welcome #channel```"))
            user, db = await sql.c()
            await db.execute("SELECT * FROM welcome WHERE guild=%s", (ctx.guild.id,))
            data = await db.fetchone()
            if data:
                channel32 = self.client.get_channel(data[1])
                msg = await ctx.send(embed=discord.Embed(color=SETTINGS.embedcolor,
                                                         description=f"Your current Welcome Channel is: {channel32.name}\nDo you want to overwrite it? React with ✅"))
                await msg.add_reaction("✅")
                await self.client.wait_for("raw_reaction_add", timeout=120,
                                           check=lambda p: p.user_id == ctx.author.id and str(
                                               p.emoji) == "✅" and p.channel_id == ctx.channel.id)
            await db.execute("DELETE FROM welcome WHERE guild=%s", (ctx.guild.id,))
            await db.execute("INSERT INTO welcome VALUE (%s, %s)", (ctx.guild.id, channel.id,))
            await ctx.send(embed=discord.Embed(color=SETTINGS.embedsuccess,
                                               description=f"Your Welcome Channel was successfully set to {channel.mention}"))
            await user.commit()
            await db.commit()
            user.close()
        else:
            return await ctx.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                      description=f"You need Admin Permissions."))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        user, db = await sql.c()
        await db.execute("SELECT * FROM welcome WHERE guild=%s", (member.guild.id,))
        data = await db.fetchone()
        user.close()
        await db.close()
        if data:
            Log = self.client.get_channel(data[1])
            embed = discord.Embed(title=f"Welcome `{member.display_name}` to {member.guild.name}!", color=0x1df221)
            embed.add_field(name="Joined at", value=f"{member.joined_at.__format__('%A, %B %d, %Y')}")
            embed.set_thumbnail(url=member.avatar_url)
            is_new = member.created_at > (datetime.datetime.utcnow() - datetime.timedelta(days=7))
            if is_new:
                embed.add_field(name="**New Account**", value=member.created_at.__format__('%A, %B %d, %Y'),
                                inline=False)
            await Log.send(embed=embed)


def setup(client):
    client.add_cog(welcome(client))
