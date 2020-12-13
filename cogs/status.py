import json

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS
from modules import sql


class status(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.checkstore.start()
        except:
            self.checkstore.stop()
            self.checkstore.start()

    @tasks.loop(seconds=30)
    async def checkstore(self):
        CachedStatus = json.loads(
            await (await aiofiles.open('Cache/Status.json', mode='r')).read())  # Load the cached status
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://ft308v428dv3.statuspage.io/api/v2/components.json') as data:
                Status = await data.json()
        NewStatus = {}
        for i in Status["components"]:
            # Website
            if i["id"] == "l483xcldq6qk":
                NewStatus["Website"] = i["status"]
            # Game Services
            if i["id"] == "t9xpn32q9jlb":
                NewStatus["Game Services"] = i["status"]
            # Login
            if i["id"] == "gp7pb08zbsm1":
                NewStatus["Login"] = i["status"]
            # Parties, Friends, and Messaging
            if i["id"] == "h591868l4p8r":
                NewStatus["Parties, Friends, and Messaging"] = i["status"]
            # Voice Chat
            if i["id"] == "12xt5b2ysxtk":
                NewStatus["Voice Chat"] = i["status"]
            # Matchmaking
            if i["id"] == "n62jd9mnxgnf":
                NewStatus["Matchmaking"] = i["status"]
            # Stats and Leaderboards
            if i["id"] == "x6np52ybtwrv":
                NewStatus["Stats and Leaderboards"] = i["status"]
            # Item Shop
            if i["id"] == "689s95gldrs3":
                NewStatus["Item Shop"] = i["status"]
        if CachedStatus != NewStatus:
            if Settings.SETTINGS.test is True:
                return
            await (await aiofiles.open('Cache/Status.json', mode='w+')).write(
                json.dumps(NewStatus, indent=2))  # Overwrite the old status
            print("New Status")
            print(NewStatus)
            temp = await sql.c()
            myuser = temp[0]
            mydb = temp[1]
            await mydb.execute("SELECT * FROM status")
            data = await mydb.fetchall()
            await mydb.close()
            myuser.close()
            counter = 0
            for i in data:
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
                    async with aiohttp.ClientSession() as ses:
                        async with ses.get(
                                "https://lightswitch-public-service-prod06.ol.epicgames.com/lightswitch/api/service/bulk/status?serviceId=Fortnite") as resp:
                            if resp.status != 200:
                                text = "Fortnite doesnt answere."
                            text = (await resp.json())[0]["message"]
                    embed.set_footer(text=text)
                    embed.add_field(value=f"{emoji} **-** {NewStatus[i2]}", name=f"{i2}", inline=False)
                channel = self.client.get_channel(i[1])
                if not channel:
                    continue
                try:
                    message = await channel.fetch_message(i[2])
                    if not message:
                        msg = await channel.send(embed=embed)
                        temp = await sql.c()
                        myuser = temp[0]
                        mydb = temp[1]
                        await mydb.execute("DELETE FROM status where channel=%s", (i[1],))
                        await mydb.execute("INSERT INTO status VALUE (%s, %s, %s)", (i[0], i[1], msg.id,))
                        await myuser.commit()
                        await mydb.close()
                        myuser.close()
                        print("Status send")
                    await message.edit(embed=embed)
                except:
                    try:
                        msg = await channel.send(embed=embed)
                        temp = await sql.c()
                        myuser = temp[0]
                        mydb = temp[1]
                        await mydb.execute("DELETE FROM status where channel=%s", (i[1],))
                        await mydb.execute("INSERT INTO status VALUE (%s, %s, %s)", (i[0], i[1], msg.id,))
                        await myuser.commit()
                        await mydb.close()
                        print("Status send")
                    except Exception as ex:
                        print(ex)

    def cog_unload(self):
        self.checkstore.stop()
        print("status LOOP BEENDET")
        try:
            self.client.unload_extension("cogs.status")
        except:
            print("CANOT UNLOAD EXTENSION status")
        try:
            self.client.load_extension("cogs.status")
        except:
            print("CANOT RELOAD EXTENSION status")


def setup(client):
    client.add_cog(status(client))
