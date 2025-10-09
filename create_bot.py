from aiogram import Bot, Dispatcher
import os
from aiogram.fsm.storage.memory import MemoryStorage

storage=MemoryStorage()

bot = Bot(token='')
#bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=storage)

