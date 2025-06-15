from aiogram.fsm.state import StatesGroup, State


class StartKeyboardStates(StatesGroup):
    get_lot = State()
    choose_auction = State()