import types

from aiogram import Router, F, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from create_bot import bot
from data_base import sqllite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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


@admin_router.callback_query(F.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    pizza_name = callback_query.data.replace('del ', '')
    await sqllite_db.sql_delete_command(pizza_name)
    await callback_query.answer(text=f'{pizza_name} удалена.', show_alert=True)



@admin_router.message(Command("Удалить"), StateFilter(FSMAdmin))
async def delete_item(message, state: FSMContext):
    if message.from_user.id == ID:
        read = await sqllite_db.sql_read2()
        for ret in read:
            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=ret[0],
                caption=f"{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[3]}"
            )
            await bot.send_message(
                chat_id=message.from_user.id,
                text='^^^',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[1]}',\
                                                                             callback_data=f'del {ret[1]}'))
            )