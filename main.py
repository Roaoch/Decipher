import asyncio
import os
import wordsegment

from src.bot.bot_markup import menu_inline, menu_keyboard
from src.bot.chipher import router as chiper_router
from src.bot.break_in import router as break_in_router
from src.dcipher import Decipher
from src.test import text_var_2_1, \
    text_var_2_2, \
    text_var_2_3, \
    text_var_2_4, \
    text_var_2_5, \
    text_var_2_6, \
    text_var_2_7, \
    text_var_2_8, \
    text_var_2_9, \
    text_var_2_10, \
    text_var_2_11, \
    text_var_2_12, \
    text_var_2_13, \
    text_var_2_14, \
    text_var_2_15, \
    text_var_2_16, \
    text_var_2_17, \
    text_var_2_18, \
    text_var_2_19

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

wordsegment.load()

load_dotenv()

TOKEN = os.getenv('bot_api')

router = Router()

async def main():
    bot = Bot(
        token=TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp['decipher'] = Decipher()
    dp['test_texts'] = [
        text_var_2_1,
        text_var_2_2,
        text_var_2_3,
        text_var_2_4,
        text_var_2_5,
        text_var_2_6,
        text_var_2_7,
        text_var_2_8,
        text_var_2_9,
        text_var_2_10,
        text_var_2_11,
        text_var_2_12,
        text_var_2_13,
        text_var_2_14,
        text_var_2_15,
        text_var_2_16,
        text_var_2_17,
        text_var_2_18,
        text_var_2_19
    ]
    dp.include_routers(
        chiper_router,
        break_in_router,
        router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot, 
        allowed_updates=dp.resolve_used_update_types()
    )

# Больше 350 символов

# decipher = Decipher()
# all_texts = [
#     text_var_2_1,
#     text_var_2_2,
#     text_var_2_3,
#     text_var_2_4,
#     text_var_2_5,
#     text_var_2_6,
#     text_var_2_7,
#     text_var_2_8,
#     text_var_2_9,
#     text_var_2_10,
#     text_var_2_11,
#     text_var_2_12,
#     text_var_2_13,
#     text_var_2_14,
#     text_var_2_15,
#     text_var_2_16,
#     text_var_2_17,
#     text_var_2_18,
#     text_var_2_19
# ]

# for text in all_texts:
#     text, key, other = decipher.break_in(cipher_text=text)
#     print(key)

# print(decipher.dechiper(decipher.chiper("ОНИДЕТПОАЛЛЕЕВПАРК", "КЛАРНЕТ"), "КЛАРНЕТ"))


@router.message(Command('start'))
async def start(msg: Message):
    await msg.answer(
        'Шалом, я бот для взлома, дешифровки и расшифровки текстов на русском и наглийском языках методом Касиски\
            \nМой код:',
        reply_markup=menu_inline
    )
    await msg.answer('Воспользуйтесь клавиатурой, чтобы выбрать опцию', reply_markup=menu_keyboard)

@router.message(F.text)
async def start(msg: Message):
    await msg.answer('<b>Сначала</b> воспользуйтесь клавиатурой, чтобы выбрать опцию', reply_markup=menu_keyboard)

if __name__ == "__main__":
    asyncio.run(main())