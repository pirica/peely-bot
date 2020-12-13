import discord


async def add_many(emojis: list, message: discord.Message, client):
    for i in emojis:
        if client.weiter[message.id]:
            try:
                await message.add_reaction(i)
            except:
                pass
        else:
            break


async def remove_many(emojis: list, message: discord.Message, client):
    for i in emojis:
        try:
            await message.add_reaction(i)
        except:
            pass
