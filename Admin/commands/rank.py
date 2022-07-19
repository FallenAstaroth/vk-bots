from config import bot_id, owner
from utils.variables import api, db, admins_ids


def setup(handler):

    @handler.on_message(commands=["повысить", r"повысить (.*)"])
    async def rank(message):

        user_ids = await api.get_ids(message.text)

        if message.from_id == owner:

            if message.reply_message is not None:
                user_ids.append(message.reply_message.from_id)

            if len(user_ids) <= 0:
                await api.message_send(message.peer_id, "❎ Пользователь не указан.")

            else:

                done_ids = []
                skip_ids = []

                user_ids = await api.users_get(user_ids)

                for user in user_ids:

                    if user.id not in admins_ids and user.id != -bot_id:

                        admins_ids.append(user.id)
                        await db.add_admin(user.id, f"{user.first_name} {user.last_name}")
                        done_ids.append(user.id)

                    else:
                        skip_ids.append(user.id)

                if len(done_ids) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(done_ids, "rank_done"))

                if len(skip_ids) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(skip_ids, "rank_skip"))

        else:
            await api.message_send(message.peer_id, "❎ Вы не являетесь администратором.")

    @handler.on_message(commands=["понизить", r"понизить (.*)"])
    async def unrank(message):

        user_ids = await api.get_ids(message.text)

        if message.from_id == owner:

            if message.reply_message is not None:
                user_ids.append(message.reply_message.from_id)

            if len(user_ids) <= 0:
                await api.message_send(message.peer_id, "❎ Пользователь не указан.")

            else:

                done_ids = []
                skip_ids = []

                for user in user_ids:

                    if user in admins_ids:

                        admins_ids.remove(user)
                        await db.del_admin(user)
                        done_ids.append(user)

                    else:
                        skip_ids.append(user)

                if len(done_ids) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(done_ids, "unrank_done"))

                if len(skip_ids) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(skip_ids, "unrank_skip"))

        else:
            await api.message_send(message.peer_id, "❎ Вы не являетесь администратором.")

    @handler.on_message(commands=["админы"])
    async def admins(message):

        admins = await db.get_admins()

        if len(admins) > 0:

            admins_list = [f"{index + 1}) [id{admin[0]}|{admin[1]}]" for index, admin in enumerate(admins)]
            await api.message_send(message.peer_id, f"✅ Список администраторов:\n" + "\n".join(admin for admin in admins_list))

        else:
            await api.message_send(message.peer_id, "❎ Администраторы отсутствуют.")
