import logging
from typing import Type

from gtts import gTTS
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from tempfile import mkstemp
from io import BytesIO

import config
import messages

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)

language = 'ru'


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(messages.start())


def text_to_audio(text: str):
    bytes_file = BytesIO()
    audio = gTTS(text=text, lang=language)
    audio.write_to_fp(bytes_file)
    bytes_file.seek(0)
    return bytes_file


@dp.message_handler()
async def echo_message(massage: types.Message):
    voice = text_to_audio(massage.text)
    await bot.send_audio(massage.from_user.id, voice)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
