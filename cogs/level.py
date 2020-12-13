import discord
from discord.ext import commands

from modules import sql


class level(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        user, db = await sql.c()
        await db.execute("DELETE FROM lvlcd")
        await user.commit()
        await db.close()
        user.close()

    @commands.command(aliases=["level", "xp"], usage="Shows you the current level of your / or a tagged user")
    async def rank(self, ctx, member: discord.Member = None):
        user, db = await sql.c()
        await db.execute("SELECT * FROM levelinfo WHERE guild=%s", (ctx.guild.id,))
        enabled = await db.fetchone()
        if enabled:
            if member is None:
                member = ctx.author
            await db.execute("SELECT * from level WHERE id=%s AND guild=%s", (member.id, ctx.guild.id,))
            data = await db.fetchone()
            newmember = self.client.get_user(member.id)
            if newmember.bot is True:
                embed = discord.Embed(colour=0xE80A0A, description=f"{member.mention} This person has not yet leveled.")
            else:
                if data:
                    level = int(data[1] / 250)
                    xp = data[1] - level * 250
                    k_xp = data[1]
                    cl = member.colour
                    embed = discord.Embed(colour=cl)
                    embed.add_field(name='Level:', value=f'{level}')
                    embed.add_field(name='XP:', value=f"{xp}/250")
                    embed.add_field(name='All XP:', value=f'{k_xp}')
                else:
                    embed = discord.Embed(colour=0xE80A0A,
                                          description=f"{member.mention} has not yet leveled.")
        else:
            await db.close()
            user.close()
            return await ctx.send("The level system is currently deactivated on this server. If you are an staff "
                                  "member of this server, you can activate it in our dashboard. "
                                  "https://peely.de/login")
        await db.close()
        user.close()
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(level(client))
