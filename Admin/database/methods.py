from aiosqlite import connect


class Database:

    def __init__(self, database: str):

        self.database = database

    async def get_admins(self):

        async with connect(self.database) as db:
            async with db.execute("SELECT * FROM admins") as cursor:

                return await cursor.fetchall()

    async def add_admin(self, user_id: int, name: str):

        async with connect(self.database) as db:

            await db.execute("INSERT INTO admins(user_id, name) VALUES (%d, '%s')" % (user_id, name))
            await db.commit()

    async def del_admin(self, user_id: int):

        async with connect(self.database) as db:

            await db.execute("DELETE FROM admins WHERE user_id = %d" % user_id)
            await db.commit()

    async def check_user_banlist(self, user_id: int):

        async with connect(self.database) as db:
            async with db.execute("SELECT count(user_id) FROM banlist WHERE user_id = %d" % user_id) as cursor:

                result = await cursor.fetchone()

                if result[0] == 0:
                    return False

                else:
                    return True

    async def insert_user_banlist(self, user_id: int):

        async with connect(self.database) as db:

            await db.execute("INSERT INTO banlist(user_id) VALUES (%d)" % user_id)
            await db.commit()

    async def delete_user_banlist(self, user_id: int):

        async with connect(self.database) as db:

            await db.execute("DELETE FROM banlist WHERE user_id = %d" % user_id)
            await db.commit()

    async def get_banned_users(self):

        async with connect(self.database) as db:
            async with db.execute("SELECT * FROM banlist") as cursor:

                result = await cursor.fetchall()

                if len(result) > 0:
                    return [user[0] for user in result]

                else:
                    return []

    async def insert_banword(self, banword: str):

        async with connect(self.database) as db:

            await db.execute("INSERT INTO banwords(banword) VALUES ('%s')" % banword)
            await db.commit()

    async def delete_banword(self, banword: str):

        async with connect(self.database) as db:

            await db.execute("DELETE FROM banwords WHERE banword = '%s'" % banword)
            await db.commit()

    async def get_banwords(self):

        async with connect(self.database) as db:
            async with db.execute("SELECT * FROM banwords") as cursor:

                return await cursor.fetchall()

    async def insert_user_warnlist(self, user_id: int):

        async with connect(self.database) as db:

            await db.execute("INSERT INTO warnlist(user_id, warns) VALUES (%d, 1)" % user_id)
            await db.commit()

    async def update_user_warnlist(self, user_id: int):

        async with connect(self.database) as db:

            await db.execute("UPDATE warnlist SET warns = warns + 1 WHERE user_id = %d" % user_id)
            await db.commit()

    async def delete_user_warnlist(self, user_id: int):

        async with connect(self.database) as db:

            await db.execute("DELETE FROM warnlist WHERE user_id = %d" % user_id)
            await db.commit()

    async def get_warnned_users(self):

        async with connect(self.database) as db:
            async with db.execute("SELECT * FROM warnlist") as cursor:

                return await cursor.fetchall()

    async def get_settings(self):

        async with connect(self.database) as db:
            async with db.execute("SELECT * FROM settings") as cursor:

                return [setting for setting in await cursor.fetchone()]

    async def update_warns_settings(self, warns: int):

        async with connect(self.database) as db:

            await db.execute("UPDATE settings SET warns = %d" % warns)
            await db.commit()

    async def update_greeting_settings(self, greeting: str):

        async with connect(self.database) as db:

            await db.execute("UPDATE settings SET greeting = '%s'" % greeting)
            await db.commit()

    async def update_links_settings(self, links: int):

        async with connect(self.database) as db:

            await db.execute("UPDATE settings SET links = %d" % links)
            await db.commit()
