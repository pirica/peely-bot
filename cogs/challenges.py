import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import SECRETS
from Settings import SETTINGS


async def check(ctx):
    try:
        await ctx.message.delete()
    except Exception as ex:
        print("No rights!", ex)
        pass
    if ctx.author.id == SETTINGS.nono:
        return True
    else:
        return False


class challenges(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.checkchallenges.start()
        except:
            self.checkchallenges.stop()
            self.checkchallenges.start()

    @tasks.loop(minutes=10)
    async def checkchallenges(self):
        await self.client.wait_until_ready()
        try:
            async with aiohttp.ClientSession() as cs:
                parameter = {"Authorization": SECRETS.fortniteio}
                async with cs.get(
                        'https://fortniteapi.io/challenges?season=current&lang=en', headers=parameter) as data:
                    if data.status != 200:
                        return
                    await (await aiofiles.open('Cache/challenges.json', mode='w+')).write(
                        json.dumps(await data.json(), indent=2))
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            print(ex)
            return

    @commands.command(usage=f"Show the current Challenges. | >challenges <week number>")
    async def challenges(self, ctx, weeknumber: str = None):
        if weeknumber is None:
            return await ctx.send(
                embed=discord.Embed(color=SETTINGS.embederror,
                                    description=f"You need to enter a Week number. Usage ``>challenges 1``"))
        Cached = json.loads(
            await (await aiofiles.open('Cache/challenges.json', mode='r')).read())
        try:
            if Cached["weeks"][weeknumber]:
                embed = discord.Embed(color=0x00da08, title=Cached["weeks"][weeknumber]["name"])
                for challenge in Cached["weeks"][weeknumber]["challenges"]:
                    string = ""
                    name = challenge["title"]

                    stars = challenge["stars"]
                    if stars != 0:
                        string += f"Stars: {stars}\n"
                    xp = challenge["xp"]
                    if xp != 0:
                        string += f"XP: {xp}"
                    embed.add_field(name=f"{name} (0/{challenge['progress_total']})", value=string)
                await ctx.send(embed=embed)
            else:
                raise KeyError
        except KeyError:
            str = ""
            for i in dict(Cached["weeks"]).keys():
                str += f"{i}, "
            return await ctx.send(embed=discord.Embed(color=SETTINGS.embederror, description=f"This week doesnt "
                                                                                             f"exist. Weeks: {str} | "
                                                                                             f"Usage ``>challenges "
                                                                                             f"1``"))

    def cog_unload(self):
        self.checkchallenges.stop()
        print("challenges LOOP BEENDET")
        try:
            self.client.unload_extension("cogs.challenges")
        except:
            print("CANOT UNLOAD EXTENSION challenges")
        try:
            self.client.load_extension("cogs.challenges")
        except:
            print("CANOT RELOAD EXTENSION challenges")


def setup(client):
    client.add_cog(challenges(client))
