from aiogram import types, Router
from utils.keyboards import start_keyboard
from database import add_user

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    add_user(user_id)
    await message.answer("Добро пожаловать в BIG банк! Выберите действие:", reply_markup=start_keyboard())
