from aiogram import types, Router
from database import get_balance

router = Router()

@router.message(lambda message: message.text == "Проверить баланс")
async def check_balance(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    
    if balance is None:
        await message.answer("Ваш счет не найден. Попробуйте позже.")
    else:
        await message.answer(f"Ваш баланс: {balance:.2f} сом.")
