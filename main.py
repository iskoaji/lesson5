

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from database import init_db
from handlers.start import router as start_router
from handlers.balance import router as balance_router
from handlers.transfer import router as transfer_router
from config import TOKEN

def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(balance_router)
    dp.include_router(transfer_router)

    init_db()

    bot_commands = [
        BotCommand(command="/start", description="Запустить бота")
    ]
    bot.set_my_commands(bot_commands)

    dp.run_polling(bot)

if __name__ == "__main__":
    main()
