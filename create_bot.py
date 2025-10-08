from aiogram import Bot, Dispatcher
import os
from aiogram.fsm.storage.memory import MemoryStorage

storage=MemoryStorage()

bot = Bot(token='7373941375:AAH0TSQtktgZDOuEoiQDzeaJhhWFf_lHuQY')
#bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=storage)

