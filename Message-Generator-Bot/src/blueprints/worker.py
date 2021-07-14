from os.path import exists
from random import randint
from re import findall, sub
from time import sleep
from aiofile import AIOFile
from mc import StringGenerator
from mc.validators import words_count
from vkbottle.bot import Blueprint, Message

bp = Blueprint()


@bp.on.chat_message()
async def conversations_worker(message: Message) -> None:

    if randint(1, 5) == 3 and exists(f"conversations/{message.peer_id}.txt"):

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
                await message.answer(f"{message_result}")

    async with AIOFile(f"conversations/{message.peer_id}.txt", "a", encoding="utf-8") as file:

        text = message.text.replace("\n", " ").replace("\n\n", " ")

        if "[id" in text:

            user_ids = list(set(findall(r"\[id(\d*?)\|.*?]", text)))

            for user_id in user_ids:
                text = sub(rf"\[id{user_id}\|.*?]", f"@id{user_id}", text)

        text = text.split(" ")

        if len(text) in range(1, 3):

            result = ' '.join(word for word in text)

        elif len(text) in range(3, 9):

            if bool(len(text) & 1) is False:

                number = len(text) / 2

            else:

                number = (len(text) + 1) / 2

            state = 0

            part_1 = []
            part_2 = []

            for word in text:

                if state <= number:

                    part_1.append(word)

                else:

                    part_2.append(word)

                state += 1

            part_1 = ' '.join(word for word in part_1)
            part_2 = ' '.join(word for word in part_2)

            result = f"{part_1}::{part_2}"

        else:

            index = 0
            parts = []

            while True:

                state = len(text) - index

                if state > 1:

                    parts.append(f"{text[index]} {text[index + 1]}")

                    index += 2

                else:

                    parts.append(text[index - 1])

                    break

                sleep(0.0001)

            result = '::'.join(word for word in parts)

        await file.write(f"{result}::")
