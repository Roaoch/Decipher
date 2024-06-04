from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.dcipher import Decipher
from src.bot.bot_markup import menu_keyboard

class ChipherState(StatesGroup):
    choosing_text = State()
    choosing_key = State()

router = Router()

@router.message(F.text == "Расшифровать текст")
async def handle_dechipher(msg: Message, state: FSMContext, decipher: Decipher):
    await state.update_data({
        "method": "dechiper"
    })
    await msg.answer(
        "Хорошо, тогда отправьте текст, который вы хотите расшифровать",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ChipherState.choosing_text)

@router.message(F.text == "Зашифровать текст")
async def handle_chipher(msg: Message, state: FSMContext, decipher: Decipher):
    await state.update_data({
        "method": "chiper"
    })
    await msg.answer(
        "Отправьте текст, который вы хотите зашифровать",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ChipherState.choosing_text)

@router.message(ChipherState.choosing_text, F.text)
async def handle_text(msg: Message, state: FSMContext, decipher: Decipher):
    await state.update_data({
        "text": msg.text
    })
    await msg.answer("Отправьте ключ для шифровки")
    await state.set_state(ChipherState.choosing_key)

@router.message(ChipherState.choosing_key, F.text)
async def handle_text(msg: Message, state: FSMContext, decipher: Decipher):
    user_data = await state.get_data()
    chiper_text = None
    try:
        if user_data['method'] == 'chiper':
            chiper_text = decipher.chiper(
                user_data['text'],
                msg.text
            )
        elif user_data['method'] == 'dechiper':
            chiper_text = decipher.dechiper(
                user_data['text'],
                msg.text
            )
        text = ' '.join([chiper_text[i: i+5] for i in range(0, len(chiper_text), 5)])
    except ValueError:
        text = "Текст и ключ должны бить записаны на одном языке"
    await msg.reply(
        text,
        reply_markup=menu_keyboard
    )
    await state.clear()