from vkbottle.bot import Blueprint, Message

bp = Blueprint()


@bp.on.chat_message(text=["/info", "/инфо"])
async def bot_info(message: Message) -> None:

    await message.answer("✅ Команды:\n/gen или /g - генерация ообщения\n/clear - очистка базы для беседы")
