from aiogram.fsm.state import StatesGroup, State


class CarfaxStates(StatesGroup):
    wait_for_vin = State()
