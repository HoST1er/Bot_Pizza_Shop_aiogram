from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

button_load = KeyboardButton(text = '/Загрузить')
button_delete = KeyboardButton(text = '/Удалить')


button_case_admin = [
    [
        button_load,
        button_delete
    ]
    #[b4, b5]
]

kb_admin = ReplyKeyboardMarkup(
    keyboard=button_case_admin,
    resize_keyboard=True
)

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="Отмена")]
    ]
)