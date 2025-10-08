from aiogram import types, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

from create_bot import dp, bot
from keyboards import kb_client

client_router = Router()

@client_router.message(Command(commands=['start', 'help']))
async def command_start(message):
    await message.answer('Привет! Это пиццерия', reply_markup=kb_client)

@client_router.message(Command(commands=['Режим_работы']))
async def open_command(message):
    await message.answer('Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')

@client_router.message(Command(commands=['Расположение']))
async def place_command(message):
    await message.answer('ул. Колбасная 15', reply_markup=ReplyKeyboardRemove())
