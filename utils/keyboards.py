from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Проверить баланс")],
            [KeyboardButton("Перевести средства")],
        ],
        resize_keyboard=True
    )

def transfer_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Отмена")],
        ],
        resize_keyboard=True
    )

def confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data="confirm")],
            [InlineKeyboardButton(text="Отменить", callback_data="cancel")]
        ]
    )
