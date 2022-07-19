from config import bot_id
from utils.variables import api, admins_ids


def setup(handler):

    @handler.on_message(commands=["кик", r"кик (.*)"])
    async def kick(message):

        user_ids = await api.get_ids(message.text)

        if message.from_id in admins_ids:

            if message.reply_message is not None:
                user_ids.append(message.reply_message.from_id)

            if len(user_ids) <= 0:
                await api.message_send(message.peer_id, "❎ Пользователь не указан.")

            else:

                skip_ids = []

                for user in user_ids:

                    if user not in admins_ids and user != -bot_id:

                        await api.remove_chat_user(
                            chat_id=message.peer_id - 2000000000,
                            member_id=user
                        )

                    else:
                        skip_ids.append(user)

                if len(skip_ids) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(skip_ids, "kick_skip"))

        else:
            await api.message_send(message.peer_id, "❎ Вы не являетесь администратором.")
