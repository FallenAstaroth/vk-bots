from os.path import exists
from random import randint
from aiofile import AIOFile
from mc import StringGenerator
from mc.validators import words_count
from vkbottle.bot import Blueprint, Message

bp = Blueprint()


@bp.on.chat_message(text=["/g", "/gen", "/г", "/ген"])
async def message_generator(message: Message) -> None:

    if exists(f"conversations/{message.peer_id}.txt"):

        async with AIOFile(f"conversations/{message.peer_id}.txt", encoding="utf-8") as file:

            text = await file.read()

        text_model = [sample.strip() for sample in text.split("::")]

        if len(text_model) >= 40:

            message_generator = StringGenerator(samples=text_model)

            message_parts = [
                message_generator.generate_string(
                    attempts=20,
                    validator=words_count(minimal=1, maximal=15),
                    formatter=None,
                )
                for _ in range(randint(1, 3))
            ]

            message_result = " ".join(word for word in message_parts)

            if message_result:

                await message.answer(message_result)

            else:

                await message.answer("❎ Недостаточно слов в базе")

        else:

            await message.answer("❎ Недостаточно слов в базе")

    else:

        await message.answer("❎ База ещё не создана")
