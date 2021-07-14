from random import uniform
from time import sleep

from vkbottle import API, Bot, Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, run_multibot

from config import TOKENS

bot = Bot()


@bot.on.message()
async def start_flood(message: Message):

    while True:

        await message.answer(
            "", "wall-196079784_129", keyboard=KEYBOARD_WITH_BUILDER
        )

        sleep(uniform(0.199, 0.399))


if __name__ == "__main__":
    KEYBOARD_TEXT = Text("😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😆😙😚☺🙂🤩🤗🤨🤔😐😑😶🙄😏😜🤐😔🤬😡😷😱😬😧🤤☹")
    POSITIVE = KeyboardButtonColor.POSITIVE
    NEGATIVE = KeyboardButtonColor.NEGATIVE
    KEYBOARD_WITH_BUILDER = (
        Keyboard(one_time=False, inline=False)
        .add(KEYBOARD_TEXT, color=NEGATIVE)
        .row()
        .add(KEYBOARD_TEXT, color=POSITIVE)
        .row()
        .add(KEYBOARD_TEXT, color=NEGATIVE)
        .row()
        .add(KEYBOARD_TEXT, color=POSITIVE)
        .row()
        .add(KEYBOARD_TEXT, color=NEGATIVE)
        .row()
        .add(KEYBOARD_TEXT, color=POSITIVE)
        .row()
        .add(KEYBOARD_TEXT, color=NEGATIVE)
        .row()
        .add(KEYBOARD_TEXT, color=POSITIVE)
        .row()
        .add(KEYBOARD_TEXT, color=NEGATIVE)
        .row()
        .add(KEYBOARD_TEXT, color=POSITIVE)
        .get_json()
    )
    apis = (API(token) for token in TOKENS)
    run_multibot(bot, apis=apis)
