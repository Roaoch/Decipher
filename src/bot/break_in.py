from typing import List

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.dcipher import Decipher
from src.bot.bot_markup import menu_keyboard, break_inline

class BreakState(StatesGroup):
    choosing_text = State()

router = Router()

@router.message(F.text == "Взломать шифро-текст")
async def handle_brak_in(msg: Message, state: FSMContext):
    await state.update_data({
        "mode": "test"
    })
    await msg.answer(
        "Введите свой текст или выберите из заготовленных",
        reply_markup=ReplyKeyboardRemove()
    )
    await msg.answer(
        "Тестовые шифры",
        reply_markup=break_inline
    )
    await state.set_state(BreakState.choosing_text)

@router.callback_query(BreakState.choosing_text, F.data.startswith("testbreak_"))
async def handle_get_test(callback: CallbackQuery, state: FSMContext, test_texts: List[str], decipher: Decipher):
    index = int(callback.data.split('_')[1])
    original_text = test_texts[index]
    chiphr_text = ' '.join([original_text[i: i+5] for i in range(0, len(original_text), 5)])

    dechiphr_text, key, other = decipher.break_in(cipher_text=original_text)
    dechiphr_text = ' '.join([dechiphr_text[i: i+5] for i in range(0, len(dechiphr_text), 5)])
    other = "\n".join([other_var[0] for other_var in other])
    await callback.message.answer(f'Шифро-текст')
    await callback.message.answer(f'{chiphr_text}')
    await callback.message.answer(f'Расшифровка')
    await callback.message.answer(f'{dechiphr_text}')
    await callback.message.answer(f'Самый вероятный ключ к тексту - {key}')
    await callback.message.answer(
        f'Другие возможные варинаты:\n{other}',
        reply_markup=menu_keyboard
    )
    
    await state.clear()
    await callback.answer()

@router.message(BreakState.choosing_text, F.text)
async def handle_text(msg: Message, state: FSMContext, decipher: Decipher):
    try:
        text, key, other = decipher.break_in(cipher_text=msg.text)
        dechiphr_text = ' '.join([text[i: i+5] for i in range(0, len(text), 5)])
        other = "\n".join([other_var[0] for other_var in other])
        await msg.answer(f'Расшифровка')
        await msg.answer(f'{dechiphr_text}')
        await msg.answer(f'Самый вероятный ключ к тексту - {key}')
        await msg.answer(
            f'Другие возможные варинаты:\n{other}',
            reply_markup=menu_keyboard
        )
    except ValueError:
        await msg.answer(
            'Пока для взлома шифра поддерживается только русский язык',
            reply_markup=menu_keyboard
        )
    await state.clear()