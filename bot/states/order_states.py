from aiogram.fsm.state import State, StatesGroup


class CheckoutOrder(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()
    waiting_for_payment = State()
