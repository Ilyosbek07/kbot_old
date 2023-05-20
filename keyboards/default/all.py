from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🎁 ТАНЛОВДА ИШТИРОК ЭТИШ'),
        ],
        [
            KeyboardButton(text='🎁 Совғалар'),
            KeyboardButton(text='👤 Балларим'),
        ],
        [
            KeyboardButton(text='📊 Рейтинг'),
            KeyboardButton(text='💡 Шартлар'),
        ],
        # [
        #     KeyboardButton(text='📈 Статистика')
        # ]
    ],
    resize_keyboard=True
)

number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📲 Рақамни юбориш', request_contact=True),
        ],
    ],
    resize_keyboard=True
)
