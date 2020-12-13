import aiomysql

import SECRETS


async def c():
    myuser = await aiomysql.connect(host=SECRETS.host, port=3306,
                                    user=SECRETS.user, password=SECRETS.password, db=SECRETS.db, autocommit=True)
    mydb = await myuser.cursor()
    await mydb.execute("SET NAMES utf8mb4")
    return [myuser, mydb]


async def sqlsetup():
    user, db = await c()
    await db.execute("CREATE TABLE IF NOT EXISTS shop ("
                     "guild bigint not null,"
                     "channel bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS twitteruser ("
                     "userid bigint not null,"
                     "apikey longtext not null,"
                     "apisecretkey longtext not null,"
                     "apiaccesstoken longtext not null,"
                     "apiaccesstokensecret longtext not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS lastshop ("
                     "channel bigint not null,"
                     "message bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS lastleaks ("
                     "channel bigint not null,"
                     "message bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS news ("
                     "guild bigint not null,"
                     "channel bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS leaks ("
                     "guild bigint not null,"
                     "channel bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS customgames ("
                     "guild bigint not null,"
                     "channel bigint not null,"
                     "roleid bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS status ("
                     "guild bigint not null,"
                     "channel bigint not null,"
                     "message bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS statsuser ("
                     "id bigint not null,"
                     "epicid longtext not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS webuser ("
                     "user_id bigint not null,"
                     "xtoken longtext not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS footer ("
                     "id bigint not null,"
                     "content longtext not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS fun ("
                     "id bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS webcooldown ("
                     "id bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS joinrole ("
                     "gid bigint not null,"
                     "rid bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS disabledspamfilter ("
                     "guild bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS prefix ("
                     "guild bigint not null,"
                     "prefix longtext not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS logging ("
                     "guild bigint not null,"
                     "channel bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS welcome ("
                     "guild bigint not null,"
                     "channel bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS level ("
                     "id bigint not null,"
                     "xp bigint not null,"
                     "guild bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS levelinfo ("
                     "guild bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS lvlcd ("
                     "guild bigint not null,"
                     "id bigint not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS customcommand ("
                     "guild bigint not null,"
                     "name longtext not null,"
                     "message longtext not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS warnings ("
                     "id bigint not null,"
                     "guildid bigint not null,"
                     "reason longtext"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS remindlist ("
                     "id bigint not null,"
                     "itemid longtext not null"
                     ")")

    await db.execute("CREATE TABLE IF NOT EXISTS rr ("
                     "guild bigint not null,"
                     "channel bigint not null,"
                     "message bigint not null,"
                     "role bigint not null,"
                     "emoji longtext"
                     ")")

    await db.execute("DELETE FROM webcooldown")

    await db.close()
    await user.commit()
    user.close()
    print(f"MYSQL/MARIADB wurde erfolgreich geladen.")
