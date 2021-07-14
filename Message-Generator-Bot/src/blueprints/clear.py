from os import remove
from os.path import exists
from vkbottle.bot import Blueprint, Message

bp = Blueprint()


@bp.on.chat_message(text=["/clear", "/очистка"])
async def bot_info(message: Message) -> None:

    try:

        users_list = await message.ctx_api.messages.get_conversation_members(
            peer_id=message.peer_id
        )

        admins = [i.member_id for i in users_list.items if i.is_admin is True]

        if message.from_id in admins:

            if exists(f"conversations/{message.peer_id}.txt"):

                remove(f"conversations/{message.peer_id}.txt")
                await message.answer("✅ База очищена")

            else:

                await message.answer("❎ Базы для этой беседы не существует")

        else:

            await message.answer("❎ Вы не являетесь администратором")

    except Exception:

        await message.answer("❎ Не удалось проверить пользователя, для этого мне нужны права администратора.")
