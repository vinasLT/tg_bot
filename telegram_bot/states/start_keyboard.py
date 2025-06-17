from aiogram.fsm.state import StatesGroup, State


class StartKeyboardStates(StatesGroup):
    wait_for_vin_or_lot = State()