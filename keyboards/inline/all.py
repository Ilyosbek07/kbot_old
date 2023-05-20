from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

check_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="- about me", url='https://t.me/about_me')
        ],
        [
            InlineKeyboardButton(text="Okean | محيط", url='https://t.me/photo_okeanss')
        ],
        [
            InlineKeyboardButton(text="Taskinim | تَسْكِنِمْ", url='https://t.me/taskinim')
        ],
        [
            InlineKeyboardButton(text="HEYALIM 🌼 Rasmiy", url='https://t.me/Heyalim ')
        ],
        [
            InlineKeyboardButton(text="Habibim🌿🌸", url='https://t.me/habibim_m')
        ],
        [
            InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs")
        ]

    ]
)

invite_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Одам таклиф қилиб балларни тўплаш", callback_data="invite")
        ]

    ]
)
