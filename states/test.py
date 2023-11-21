from aiogram.dispatcher.filters.state import StatesGroup, State


class Get_Prompt(StatesGroup):
    text = State()


class Edit_Prompt(StatesGroup):
    text = State()
