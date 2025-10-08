from aiogram import types
from aiogram.client import bot
from aiogram.filters import Command
from create_bot import dp, bot

@dp.message(Command(commands=['start', 'help']))
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет! Это пиццерия')
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\n@bot_pizza_shop_bot')


@dp.message(Command(commands=['Режим_работы']))
async def open_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')

@dp.message(Command(commands=['Расположение']))
async def place_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'ул. Колбасная 15')