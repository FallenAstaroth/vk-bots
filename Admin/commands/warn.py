from config import bot_id
from utils.variables import api, db, settings, admins_ids


def setup(handler):

    @handler.on_message(commands=["варн", r"варн (.*)"])
    async def warn(message):

        user_ids = await api.get_ids(message.text)

        if message.from_id in admins_ids:

            if message.reply_message is not None:
                user_ids.append(message.reply_message.from_id)

            if len(user_ids) <= 0:
                await api.message_send(message.peer_id, "❎ Пользователь не указан.")

            else:

                done_ids = []
                skip_ids = []
                warned_users = {}
                warns = settings[1]

                [warned_users.update({user[0]: {"warns": user[1]}}) for user in await db.get_warnned_users()]

                for user in user_ids:

                    if user not in admins_ids and user != -bot_id:

                        if warned_users.get(user) is None:

                            await db.insert_user_warnlist(user)
                            done_ids.append((user, f"1/{warns}"))

                        elif warned_users.get(user).get("warns") < warns - 1:

                            await db.update_user_warnlist(user)
                            done_ids.append((user, f"{warned_users.get(user).get('warns') + 1}/{warns}"))

                        else:

                            await db.delete_user_warnlist(user)
                            done_ids.append((user, f"{warns}/{warns}"))
                            await api.remove_chat_user(chat_id=message.peer_id - 2000000000, member_id=user)

                    else:
                        skip_ids.append((user, warned_users.get(user).get("warns")))

                if len(done_ids) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(done_ids, "warn_done"))

                if len(skip_ids) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(skip_ids, "warn_skip"))

        else:
            await api.message_send(message.peer_id, "❎ Вы не являетесь администратором.")

    @handler.on_message(commands=["анварн", r"анварн (.*)"])
    async def unwarn(message):

        user_ids = await api.get_ids(message.text)

        if message.from_id in admins_ids:

            if message.reply_message is not None:
                user_ids.append(message.reply_message.from_id)

            if len(user_ids) <= 0:
                await api.message_send(message.peer_id, "❎ Пользователь не указан.")

            else:

                done_ids = []
                skip_ids = []
                warned_users = [user[0] for user in await db.get_warnned_users()]

                for user in user_ids:

                    if user in warned_users:

                        await db.delete_user_warnlist(user)
                        done_ids.append(user)

                    else:
                        skip_ids.append(user)

                if len(done_ids) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(done_ids, "unwarn_done"))

                if len(skip_ids) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(skip_ids, "unwarn_skip"))

        else:
            await api.message_send(message.peer_id, "❎ Вы не являетесь администратором.")
