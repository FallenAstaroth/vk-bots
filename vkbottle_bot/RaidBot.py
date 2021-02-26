import time
import random
from config import *
from vkbottle.api import API
from vkbottle.bot import Bot, Message, run_multibot

bot = Bot()


@bot.on.message()
async def start_flood(message: Message):

    while True:

        sleep = random.uniform(0.199, 0.399)

        await message.answer("", "wall-196079784_129")

        time.sleep(sleep)


run_multibot(bot, apis=(API(TOKENS[0]), API(TOKENS[1])))
