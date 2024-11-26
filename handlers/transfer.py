from aiogram import types, Router, F
from aiogram import FSMContext
from aiogram import State, StatesGroup
from database import get_balance, set_balance, record_transfer
from utils.keyboards import confirm_keyboard, transfer_keyboard

router = Router()

class TransferState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_recipient = State()

@router.message(lambda message: message.text == "Перевести средства")
async def transfer_start(message: types.Message, state: FSMContext):
    await message.answer("Введите сумму для перевода:")
    await state.set_state(TransferState.waiting_for_amount)

@router.message(TransferState.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        user_id = message.from_user.id
        balance = get_balance(user_id)
        
        if amount <= 0:
            await message.answer("Сумма перевода должна быть больше нуля.")
            return
        
        if amount > balance:
            await message.answer("У вас недостаточно средств для перевода.")
            return
        
        await state.update_data(amount=amount)
        await message.answer("Введите ID получателя:")
        await state.set_state(TransferState.waiting_for_recipient)
    
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму.")

@router.message(TransferState.waiting_for_recipient)
async def process_recipient(message: types.Message, state: FSMContext):
    recipient_id = message.text
    data = await state.get_data()
    amount = data["amount"]
    
    if not recipient_id.isdigit():
        await message.answer("Пожалуйста, введите корректный ID получателя.")
        return
    
    user_id = message.from_user.id
    recipient_id = int(recipient_id)
    
    balance = get_balance(user_id)
    
    if balance < amount:
        await message.answer("Недостаточно средств для перевода.")
        return
    
    await state.update_data(recipient_id=recipient_id)
    await message.answer(f"Вы хотите перевести {amount} руб. пользователю с ID {recipient_id}. Подтвердите действие:", 
                         reply_markup=confirm_keyboard())
    await state.set_state(TransferState.waiting_for_confirmation)

@router.callback_query(lambda call: call.data == "confirm")
async def confirm_transfer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]
    recipient_id = data["recipient_id"]
    sender_id = call.from_user.id
    
    sender_balance = get_balance(sender_id)
    recipient_balance = get_balance(recipient_id)

    if sender_balance >= amount:
        set_balance(sender_id, sender_balance - amount)
        set_balance(recipient_id, recipient_balance + amount)
        record_transfer(sender_id, recipient_id, amount)
        
        await call.message.answer(f"Вы успешно перевели {amount} руб. пользователю с ID {recipient_id}.")
    else:
        await call.message.answer("Недостаточно средств для перевода.")
    
    await state.clear()

@router.callback_query(lambda call: call.data == "cancel")
async def cancel_transfer(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Перевод отменен.")
    await state.clear()
