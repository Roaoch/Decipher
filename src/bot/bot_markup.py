from typing import Optional

from aiogram.types import \
    InlineKeyboardButton, \
    InlineKeyboardMarkup, \
    KeyboardButton,\
    ReplyKeyboardMarkup


menu_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='GitHub', url='https://github.com/Roaoch/Decipher'),
    ]
])
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Зашифровать текст'),
            KeyboardButton(text='Расшифровать текст'),
        ],
        [
            KeyboardButton(text='Взломать шифро-текст'),
        ],
        # [
        #     KeyboardButton(text='Установить ключ')
        # ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Нажми кнопку.'
)

break_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='1', callback_data="testbreak_1"),
        InlineKeyboardButton(text='2', callback_data="testbreak_2"),
        InlineKeyboardButton(text='3', callback_data="testbreak_3"),
        InlineKeyboardButton(text='4', callback_data="testbreak_4"),        
    ],
    [
        InlineKeyboardButton(text='5', callback_data="testbreak_5"),
        InlineKeyboardButton(text='6', callback_data="testbreak_6"),
        InlineKeyboardButton(text='7', callback_data="testbreak_7"),
        InlineKeyboardButton(text='8', callback_data="testbreak_8"),
    ],
    [
        InlineKeyboardButton(text='9', callback_data="testbreak_9"),
        InlineKeyboardButton(text='10', callback_data="testbreak_10"),
        InlineKeyboardButton(text='11', callback_data="testbreak_11"),
        InlineKeyboardButton(text='12', callback_data="testbreak_12"),
    ],
    [
        InlineKeyboardButton(text='13', callback_data="testbreak_13"),
        InlineKeyboardButton(text='14', callback_data="testbreak_14"),
        InlineKeyboardButton(text='15', callback_data="testbreak_15"),
        InlineKeyboardButton(text='16', callback_data="testbreak_16"),        
    ],
    [
        InlineKeyboardButton(text='17', callback_data="testbreak_17"),
        InlineKeyboardButton(text='18', callback_data="testbreak_18"),
        InlineKeyboardButton(text='19', callback_data="testbreak_19")        
    ]
])