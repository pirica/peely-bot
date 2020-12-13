import random

import modules.sql as sql


async def get_footer():
    temp = await sql.c()
    user = temp[0]
    db = temp[1]
    await db.execute("SELECT * FROM footer")
    footers = await db.fetchall()
    user.close()
    await db.close()
    footer = random.choice(footers)
    return footer[1]
