import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message

from app.api.api import WikipediaApi
from app.controller import ApiController
from settings import TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

controller = ApiController(WikipediaApi("ru"))


@dispatcher.message_handler(commands=["start", "help"])
async def help_handler(message: Message):
    await message.reply("Hello world")


@dispatcher.message_handler()
async def main_handler(message: Message):
    x = await controller.handle_query(message.text, message)


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
