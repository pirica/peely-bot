import discord
from discord.ext import commands

from Settings import SETTINGS
from modules import sql


class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["setprefix", "newprefix", "new_prefix"], usage="Set a Custom Prefix for your Server.")
    async def set_prefix(self, ctx, prefix: str = None):
        if ctx.message.author.guild_permissions.administrator:
            if prefix is None:
                return await ctx.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                          description=f"You need to add a Prefix. ```>set_prefix >```"))
            if len(prefix) >= 4:
                return await ctx.send(
                    embed=discord.Embed(color=SETTINGS.embederror, description=f"Your prefix cannot be longer than 3"))
            user, db = await sql.c()
            await db.execute("SELECT * FROM prefix WHERE guild=%s", (ctx.guild.id,))
            data = await db.fetchone()
            if data:
                msg = await ctx.send(embed=discord.Embed(color=SETTINGS.embedcolor,
                                                         description=f"Your current prefix is: {data[1]}\nDo you want to overwrite it? React with ✅"))
                await msg.add_reaction("✅")
                await self.client.wait_for("raw_reaction_add", timeout=120,
                                           check=lambda p: p.user_id == ctx.author.id and str(
                                               p.emoji) == "✅" and p.channel_id == ctx.channel.id)
            await db.execute("DELETE FROM prefix WHERE guild=%s", (ctx.guild.id,))
            await db.execute("INSERT INTO prefix VALUE (%s, %s)", (ctx.guild.id, prefix,))
            await ctx.send(embed=discord.Embed(color=SETTINGS.embedsuccess,
                                               description=f"Your prefix was successfully set to ``{prefix}``"))
            await user.commit()
            await db.close()
            user.close()
        else:
            return await ctx.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                      description=f"You need Admin Permissions."))


def setup(client):
    client.add_cog(prefix(client))
