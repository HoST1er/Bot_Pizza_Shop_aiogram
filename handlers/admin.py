from aiogram import Router, F, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from create_bot import bot
from data_base import sqllite_db
from keyboards import admin_kb

ID=None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

admin_router = Router()

ID = None  # глобальная переменная для хранения ID админа

# --- Фильтр: только если пользователь — администратор чата ---
@admin_router.message(Command("moderator"))
async def make_changes_command(message, bot: Bot):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
        await message.reply("❌ У вас нет прав администратора!")
        return

    global ID
    ID = message.from_user.id
    await bot.send_message(ID, "Что хозяин надо???", reply_markup=admin_kb.kb_admin)
    await message.delete()
# --- Шаг 1: команда запуска ---
@admin_router.message(Command("Загрузить"), StateFilter(None))
async def cm_start(message, state: FSMContext):
    if message.from_user.id == ID:
        await state.set_state(FSMAdmin.photo)
        await message.reply("Загрузи фото")

# --- Шаг 2: загрузка фото ---
@admin_router.message(F.photo, StateFilter(FSMAdmin.photo))
async def load_photo(message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(photo=message.photo[0].file_id)
        await state.set_state(FSMAdmin.name)
        await message.reply("Теперь введи название")

# --- Шаг 3: название ---
@admin_router.message(StateFilter(FSMAdmin.name))
async def load_name(message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(name=message.text)
        await state.set_state(FSMAdmin.description)
        await message.reply("Теперь введи описание")

# --- Шаг 4: описание ---
@admin_router.message(StateFilter(FSMAdmin.description))
async def load_description(message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(description=message.text)
        await state.set_state(FSMAdmin.price)
        await message.reply("Теперь укажи цену")

# --- Шаг 5: цена и вывод всех данных ---
@admin_router.message(StateFilter(FSMAdmin.price))
async def load_price(message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(price=message.text)
        # user_data = await state.get_data()
        # if user_data:
        #     text = "\n".join(f"{key}: {value}" for key, value in user_data.items())
        #     await message.answer(f"Текущие данные:\n{text}")
        # else:
        #     await message.answer("Данных пока нет.")
        await sqllite_db.sql_add_command(state)
        await state.clear()

# --- Универсальный обработчик отмены ---
@admin_router.message(Command("Отмена"), StateFilter(FSMAdmin))
async def cancel_fsm(message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            await message.reply("FSM не активен, нечего отменять.")
            return
        await state.clear()
        await message.reply("Действие отменено. Выход из режима ввода.")