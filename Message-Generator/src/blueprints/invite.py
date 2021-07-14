from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.bot import ChatActionRule

bp = Blueprint()


@bp.on.chat_message((ChatActionRule("chat_invite_user")))
async def bot_invited(message: Message) -> None:

    if message.group_id == -message.action.member_id:

        await message.answer("✅ Начинаю работать\n\nНе забудьте выдать доступ ко всей переписке в настройках беседы, чтобы я мог видеть сообщения участников\n\nСписок команд доступен по команде /info")
