from aiogram.fsm.state import StatesGroup, State


class FindForMeStates(StatesGroup):
    #user
    wait_for_make = State()
    wait_for_model = State()
    wait_for_year_from = State()
    wait_for_year_to = State()
    wait_for_budget_from = State()
    wait_for_budget_to = State()
    wait_for_specific_message = State()
    wait_for_confirmation = State()

    #admin
    wait_for_lot_id = State()

