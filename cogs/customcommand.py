import discord
from discord.ext import commands

from Settings import SETTINGS
from modules import sql


class customcommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["createcommand", "addcommand", "add_command", "newcommand", "new_command"],
                      usage="Create a new Custom Command with your own Text.")
    async def create_command(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            msg = await ctx.send(embed=discord.Embed(color=SETTINGS.embedcolor,
                                                     description="Please send me the name of the command below this message."))
            command = await self.client.wait_for("message", timeout=120,
                                                 check=lambda
                                                     m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
            await command.delete()
            await msg.edit(embed=discord.Embed(color=SETTINGS.embedcolor,
                                               description="Please send me the response of your command below this message."))
            response = await self.client.wait_for("message", timeout=120,
                                                  check=lambda
                                                      m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
            await response.delete()
            user, db = await sql.c()
            await db.execute("DELETE FROM customcommand WHERE guild=%s AND name=%s",
                             (ctx.guild.id, str(command.content),))
            await db.execute("INSERT INTO customcommand VALUE (%s, %s, %s)",
                             (ctx.guild.id, str(command.content), str(response.content),))
            await user.commit()
            await db.close()
            user.close()
            await msg.edit(embed=discord.Embed(color=SETTINGS.embedsuccess,
                                               description="I have successfully created the command."))
        else:
            return await ctx.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                      description=f"You need Admin Permissions to do that."))

    @commands.command(aliases=["deletecommand", "delcommand", "del_command", "removecommand", "remove_command"],
                      usage="Remove a Custom Command.")
    async def delete_command(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            msg = await ctx.send(embed=discord.Embed(color=SETTINGS.embedcolor,
                                                     description="Please send me the name of the command below this message."))
            command = await self.client.wait_for("message", timeout=120,
                                                 check=lambda
                                                     m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
            await command.delete()
            user, db = await sql.c()
            await db.execute("SELECT * FROM customcommand WHERE guild=%s AND name=%s",
                             (ctx.guild.id, str(command.content),))
            data = await db.fetchone()
            if not data:
                return await msg.edit(embed=discord.Embed(color=SETTINGS.embederror,
                                                          description="This command doesnt exist."))
            db.execute("DELETE FROM customcommand WHERE guild=%s AND name=%s", (ctx.guild.id, str(command.content),))
            await user.commit()
            await db.close()
            user.close()
            await msg.edit(embed=discord.Embed(color=SETTINGS.embedsuccess,
                                               description="I have successfully deleted the command."))
        else:
            return await ctx.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                      description=f"You need Admin Permissions to do that."))


def setup(client):
    client.add_cog(customcommands(client))
