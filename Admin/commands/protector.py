from re import compile, findall

from utils.variables import api, db, settings, admins_ids, banwords
from api.data.events import Actions


link = compile(r"^(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]*$")


def setup(handler):

    @handler.on_action(actions=[Actions.ChatInviteNewUser, Actions.ChatInviteUserByLink])
    async def new_user(message):

        if await db.check_user_banlist(message.action.member_id):

            if message.from_id in admins_ids:

                await db.delete_user_banlist(message.action.member_id)
                await api.message_send(message.peer_id, "✅ Администратор пригласил забаненого пользователя. Удаляю из банлиста.")

            else:
                await api.remove_chat_user(chat_id=message.peer_id - 2000000000, member_id=message.action.member_id)

        else:

            user = (await api.users_get([message.action.member_id]))[0]
            await api.message_send(message.peer_id, f"✅ [id{message.action.member_id}|{user.first_name} {user.last_name}]\n{settings[0]}")

    @handler.default()
    async def default_event(message):

        if message.from_id in admins_ids:
            return

        if settings[2] == 1:

            for link in ["vk.com/", "https://", "http://", "vk.me/", "vk.cc/"]:
                if link in message.text.lower():

                    await api.remove_chat_user(chat_id=message.peer_id - 2000000000, member_id=message.from_id)
                    return await api.message_delete(cmids=[message.conversation_message_id], peer_id=message.peer_id, delete_for_all=1)

        if len(banwords) > 0:

            for banword in banwords:
                if banword in message.text.lower():

                    await api.message_send(message.peer_id, f"✅ Обнаружен банворд - {banword}. Исключаю пользователя.")
                    return await api.remove_chat_user(chat_id=message.peer_id - 2000000000, member_id=message.from_id)
