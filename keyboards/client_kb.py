from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton(text='/Режим работы')
b2 = KeyboardButton(text='/Расположение')
b3 = KeyboardButton(text='/Меню')
# b4 = KeyboardButton(text='/Поделиться_номером', request_contact=True)
# b5 = KeyboardButton(text='/Отправить_где_я', request_location=True)

buttons = [
    [
        b1,
        b2,
        b3
    ]
    #[b4, b5]
]

kb_client = ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True
)