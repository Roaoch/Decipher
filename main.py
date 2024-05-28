import asyncio
import os
import wordsegment

from src.dcipher import Decipher
from src.test import text_var_2_3, text_var_2_1

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
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot, 
        allowed_updates=dp.resolve_used_update_types()
    )

decipher = Decipher()
text, key = decipher.break_in(cipher_text=text_var_2_1)
decipher.dechiper(cipher_text=text_var_2_1, key=key)

print(text)
print(key)

# @router.message(Command('start'))
# async def start(msg: Message):
#     await msg.answer(
#         'Привет, я нейросеть генерирующий тексты. Я обучен на корпусе текстов Фёдора Михаайловича Достоеевского!\nSpecial thanks:\
#             \n    Фёдор Михаайлович Достоеевский\
#             \nРазработчики:\
#             \n    Горшенин А.К\
#             \n    Мыльников Н.В\
#             \n    Колин А.В\
#             \n    Закиров Р.М\
#             \n    Смирнов И.С\
#             \n    Воробъёв А.И\
#             \nМои потроха:',
#         reply_markup=menu_inline
#     )
#     await msg.answer('Чтобы сгенерировать новое предложение - нажмите на кнопку клавиатуры', reply_markup=menu_keyboard)

# @router.message(F.text == 'Сгенерировать предложение')
# async def text_handler(msg: Message):
#     await msg.answer('Подождите буквально пару секунд')
#     text = text_generator.generate()
#     await msg.answer(f'Достоевский: {text}', reply_markup=menu_keyboard)

if __name__ == "__main__":
    asyncio.run(main())