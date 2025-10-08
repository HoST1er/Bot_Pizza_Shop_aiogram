import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()  # ← здесь нужны скобки!

    if base:
        print('Data base connected OK!')

    base.execute('''
        CREATE TABLE IF NOT EXISTS menu(
            img TEXT,
            name TEXT PRIMARY KEY,
            description TEXT,
            price TEXT
        )
    ''')
    base.commit()


async def sql_add_command(state):
    data = await state.get_data()  # ✅ получаем словарь данных
    cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
    base.commit()

async def sql_read():
    @client_router.message(Command(commands=['Расположение']))
    async def place_command(message):
        await message.answer('ул. Колбасная 15')