import json
import string
from create_bot import dp, bot
from aiogram import types, F, Dispatcher, Router


#@dp.message(F.text)
# async def echo_send(message : types.Message):
#     if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(" ")}\
#         .intersection(set(json.load(open('cenz.json')))) != set():
#         await message.reply('Маты запрещены')
#         await message.delete()

other_router = Router()

@other_router.message(F.text)
async def echo_send(message : types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(" ")}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()
    # await message.answer('Привет! Это пиццерия')
# def register_handlers_other(dp : Dispatcher):
#     dp.register_message_handler(echo_send)
