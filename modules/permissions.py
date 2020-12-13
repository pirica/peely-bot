from Settings import SETTINGS


async def check(ctx):
    if ctx.author.id == SETTINGS.nono:
        return True
    else:
        return False
