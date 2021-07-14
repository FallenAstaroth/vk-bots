from os import mkdir
from os.path import exists
from config import BOT_TOKEN
from vkbottle.bot import Bot
from vkbottle import load_blueprints_from_package

if __name__ == "__main__":
    
    bot = Bot(BOT_TOKEN)

    for bp in load_blueprints_from_package("blueprints"):

        bp.load(bot)

    if not exists(f"conversations"):

        mkdir(f"conversations")

    bot.run_forever()
