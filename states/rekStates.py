from aiogram.dispatcher.filters.state import StatesGroup, State


class RekData(StatesGroup):
    choice = State()
    picture = State()
    score = State()
    text = State()
    shart = State()
    gift = State()
    add = State()
    delete = State()
    kbsh = State()
    winners = State()

class Number(StatesGroup):
    number = State()
    add_user = State()


class DelUser(StatesGroup):
    add = State()
    user = State()
    fix = State()
