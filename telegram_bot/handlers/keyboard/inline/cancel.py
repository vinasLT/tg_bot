from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

cancel_router = Router()

@cancel_router.callback_query(F.data == 'cancel')
async def cancel_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.delete()
    await state.clear()
