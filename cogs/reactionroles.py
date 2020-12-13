import random

import discord
from discord.ext import commands

import Settings.SETTINGS as SETTINGS
from modules import sql


async def check(ctx):
    try:
        await ctx.message.delete()
    except Exception as ex:
        print("No rights!", ex)
        pass
    if ctx.author.guild_permissions.manage_guild:
        return True
    elif ctx.author.id == SETTINGS.nono:
        return True
    else:
        await ctx.send(
            embed=discord.Embed(color=SETTINGS.embederror, description="You dont have permissions. (Manage Server)"))
        return False


class reactionroles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="Create a Reaction Role")
    @commands.check(check)
    async def createrr(self, ctx):
        if ctx.author.guild_permissions.manage_guild:
            for i in ctx.guild.text_channels:
                break
            embed = discord.Embed(color=SETTINGS.embedsuccess,
                                  description=f"Please send me now the channel mention like {i.mention}")
            edit = await ctx.send(embed=embed)
            msg = await self.client.wait_for("message", check=lambda
                m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=999)
            try:
                await msg.delete()
            except:
                pass
            if not msg.channel_mentions[0]:
                embed = discord.Embed(color=SETTINGS.embederror)
                embed.set_author(icon_url=ctx.author.avatar_url, url="https://peely.de",
                                 name=f"Please run the command again and tag a valid text channel like {i.mention}.")
                return await edit.edit(embed=embed)
            else:
                zahl = random.randint(111111111111111111, 999999999999999999)
                embed = discord.Embed(color=SETTINGS.embedsuccess,
                                      description=f"Please send me now a message ID like {zahl}")
                await edit.edit(embed=embed)
                msg2 = await self.client.wait_for("message", check=lambda
                    m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=999)
                messageid = msg2.content
                try:
                    await msg2.delete()
                except:
                    pass
                try:
                    message = await msg.channel_mentions[0].fetch_message(messageid)
                except:
                    embed = discord.Embed(color=SETTINGS.embederror)
                    embed.set_author(icon_url=ctx.author.avatar_url, url="https://peely.de",
                                     name=f"Please run the command again and send me a valid message id like {zahl}.")
                    return await edit.edit(embed=embed)
                if not message:
                    embed = discord.Embed(color=SETTINGS.embederror)
                    embed.set_author(icon_url=ctx.author.avatar_url, url="https://peely.de",
                                     name=f"Please run the command again and send me a valid message id like {zahl}.")
                    return await ctx.send(embed=embed)
                elif not isinstance(message, discord.Message):
                    embed = discord.Embed(color=SETTINGS.embederror)
                    embed.set_author(icon_url=ctx.author.avatar_url, url="https://peely.de",
                                     name=f"Please run the command again and send me a valid message id like {zahl}.")
                    return await edit.edit(embed=embed)
                else:
                    counter = 0
                    for i in ctx.guild.roles:
                        counter += 1
                        if counter < 1:
                            break
                    embed = discord.Embed(color=SETTINGS.embedsuccess,
                                          description=f"Please send me now a Role like {i.mention}")
                    await edit.edit(embed=embed)
                    msg2 = await self.client.wait_for("message", check=lambda
                        m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=999)
                    role = msg2.role_mentions[0]
                    if not role:
                        embed = discord.Embed(color=SETTINGS.embederror)
                        embed.set_author(icon_url=ctx.author.avatar_url, url="https://peely.de",
                                         name=f"Please run the command again and send me a valid role id like {i.mention}.")
                        return await edit.edit(embed=embed)
                    elif not isinstance(role, discord.Role):
                        embed = discord.Embed(color=SETTINGS.embederror)
                        embed.set_author(icon_url=ctx.author.avatar_url, url="https://peely.de",
                                         name=f"Please run the command again and send me a valid role id like {i.mention}.")
                        return await edit.edit(embed=embed)
                    else:
                        try:
                            await msg2.delete()
                        except:
                            pass
                        embed = discord.Embed(color=SETTINGS.embedsuccess,
                                              description=f"Please react now with the emoji that you want to use.")
                        await edit.edit(embed=embed)
                        emoji = await self.client.wait_for("raw_reaction_add", check=lambda
                            p: p.user_id == ctx.author.id and p.channel_id == ctx.channel.id, timeout=999)
                        try:
                            if emoji.emoji.is_custom_emoji():
                                await message.add_reaction(emoji=emoji.emoji)
                            else:
                                await message.add_reaction(emoji=emoji.emoji.name)
                            temp = await sql.c()
                            user = temp[0]
                            db = temp[1]
                            await db.execute("INSERT INTO rr VALUE (%s, %s, %s, %s, %s)",
                                             (ctx.guild.id, message.channel.id, message.id, role.id, str(emoji.emoji),))
                            await user.commit()
                            await db.close()
                            user.close()
                            try:
                                await edit.clear_reactions()
                            except:
                                pass
                            await edit.edit(
                                embed=discord.Embed(description=f"Sucessfull added.", color=SETTINGS.embedsuccess),
                                delete_after=6)
                        except Exception as ex:
                            await edit.edit(embed=discord.Embed(color=SETTINGS.embederror, description=f"I dont have "
                                                                                                       f"permissions."
                                                                                                       f" {ex}"))
        else:
            embed = discord.Embed(color=SETTINGS.embederror)
            embed.set_author(icon_url=ctx.author.avatar_url, url="https://peely.de", name="You dont have Permissions. "
                                                                                          "You missing the manage "
                                                                                          "guild Permissions.")
            await ctx.send(embed=embed)

    @commands.command(aliases=["delrr", "deleterr", "clearrr"], usage="Delete the Reaction Role")
    async def removerr(self, ctx, message: discord.Message = None):
        if ctx.author.guild_permissions.manage_guild:
            if message is None:
                zahl = random.randint(111111111111111111, 999999999999999999)
                return await ctx.send(embed=discord.Embed(
                    description=f"You have to enter a message ID. Use the command like this: ``>clearrr {zahl}``",
                    color=SETTINGS.embederror))
            else:
                user, db = await sql.c()
                await db.execute("DELETE FROM rr WHERE message=%s and guild=%s", (message.id, ctx.guild.id,))
                await user.commit()
                await db.close()
                user.close()
                try:
                    await message.clear_reactions()
                except:
                    pass
                await ctx.send(embed=discord.Embed(
                    description=f"Successful. I removed all reactions from the message with the id: ``{message.id}``",
                    color=SETTINGS.embedsuccess))
        else:
            embed = discord.Embed(color=SETTINGS.embederror)
            embed.set_author(icon_url=ctx.author.avatar_url, url="https://peely.de", name="You dont have Permissions. "
                                                                                          "You missing the manage "
                                                                                          "guild Permissions.")
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.client.user.id:
            return
        temp = await sql.c()
        user = temp[0]
        db = temp[1]
        if payload.emoji.is_custom_emoji():
            await db.execute("SELECT * FROM rr WHERE guild=%s", (payload.guild_id,))
        else:
            await db.execute("SELECT * FROM rr WHERE guild=%s", (payload.guild_id,))
        data = await db.fetchall()
        await db.close()
        user.close()
        for i in data:
            if i[1] == payload.channel_id:
                if i[2] == payload.message_id:
                    if str(payload.emoji) == str(i[4]):
                        guild = self.client.get_guild(payload.guild_id)
                        member = guild.get_member(payload.user_id)
                        try:
                            role = guild.get_role(i[3])
                            await member.add_roles(role)
                        except:
                            channel = self.client.get_channel(payload.channel_id)
                            await channel.send(member.mention, embed=discord.Embed(
                                description=f"I dont have permissions to give you the role.",
                                color=SETTINGS.embederror))
                        break

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.client.user.id:
            return
        temp = await sql.c()
        user = temp[0]
        db = temp[1]
        if payload.emoji.is_custom_emoji():
            await db.execute("SELECT * FROM rr WHERE guild=%s", (payload.guild_id,))
        else:
            await db.execute("SELECT * FROM rr WHERE guild=%s", (payload.guild_id,))
        data = await db.fetchall()
        await db.close()
        user.close()
        for i in data:
            if i[1] == payload.channel_id:
                if i[2] == payload.message_id:
                    if str(payload.emoji) == i[4]:
                        guild = self.client.get_guild(payload.guild_id)
                        member = guild.get_member(payload.user_id)
                        role = guild.get_role(i[3])
                        try:
                            await member.remove_roles(role)
                        except:
                            channel = self.client.get_channel(payload.channel_id)
                            await channel.send(member.mention, embed=discord.Embed(
                                description=f"I dont have permissions to remove you the role.",
                                color=SETTINGS.embederror))
                        break


def setup(client):
    client.add_cog(reactionroles(client))
