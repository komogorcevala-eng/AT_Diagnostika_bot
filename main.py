import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Router, F, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from db import create_db, add_user, get_all_users

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID_"))

bot = Bot(token=TOKEN)
r = Router()
dp = Dispatcher()
dp.include_routers(r)

# создание кнопки
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Новая рассылка")]
], resize_keyboard=True)

# FSM отправка
class sender(StatesGroup):
    photo = State()
    text = State()

@r.message(F.text == "Новая рассылка")
async def start_sender(message: Message, state: FSMContext):
    await message.answer("Отправьте фото для рассылки", reply_markup=ReplyKeyboardRemove())
    await state.set_state(sender.photo)

@r.message(sender.photo)
async def photo_handler(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer("Пришлите текст")
    await state.set_state(sender.text)

@r.message(sender.text)
async def send_all(message: Message, state: FSMContext, bot: Bot):
    text = message.text
    data = await state.get_data()
    photo_user = data.get('photo')
    users = get_all_users()
    for user_id in users:
        try:
            await bot.send_photo(user_id, photo=photo_user, caption=text)
        except Exception as error:
            print(f'Проблема: {error}')

    await message.answer('Сообщение успешно разослано')
    await state.clear()

@r.message(CommandStart())
async def start(message: Message):
    create_db()

    user_id = message.from_user.id
    username = message.from_user.username or "Нет username"
    first_name = message.from_user.first_name or "Неизвестно"

    add_user(user_id, username, first_name)

    if user_id == ADMIN_ID:
        await message.answer(
            'Привет, нажми: "Новая рассылка"',
            reply_markup=main_kb
        )
    else:
        await message.answer(
            "Здравствуйте! Этот бот будет присылать вам самые свежие акции!",
            reply_markup=ReplyKeyboardRemove()
        )

async def main():
    await dp.start_polling(bot, polling_timeout=30)

if __name__ == "__main__":
    create_db()
    asyncio.run(main())