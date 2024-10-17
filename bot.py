import asyncio
import logging
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from BashRoute import BashRoute
from ParseBash import ParseBash

# Машина состояний
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Класс аунтефикации
class UserInfo(StatesGroup):
	city_to = State()
	city_from = State()
	date = State()


# Логгирование
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="5924422521:AAGjxWWzIbqfKV2_W5SNml-7Vn0C7zFJaHM")

# Диспетчер
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Основные кнопки меню
global greet_kb
button_search = KeyboardButton('Поиск билетов')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_search)

# /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
	await message.answer(
		"Приветствую, это бот для поиска билетов БашАвтоТранс\n\n"
		"Он предназначен для просмотра актуального расписания и цен\n"
		"\n",
		reply_markup=greet_kb
	)

# Поиск маршрутов, город отправления
@dp.message_handler(lambda message: message.text == "Поиск билетов",state=None)
async def schedule(message: types.Message):
	greet_kb = ReplyKeyboardMarkup(one_time_keyboard=True)
	await message.answer('Город отправления:')
	await UserInfo.city_to.set()

# Город прибытия
@dp.message_handler(state=UserInfo.city_to)# Как только бот получит ответ, вот это выполнится
async def answer_q1(message: types.Message, state: FSMContext):
	answer = message.text
	await state.update_data(answer1=answer)# тут же он записывает наш ответ из предыдущего вопроса
	await message.answer('Город прибытия:')
	await UserInfo.city_from.set()

# Дата поездки
@dp.message_handler(state=UserInfo.city_from)# Как только бот получит ответ, вот это выполнится
async def answer_q2(message: types.Message, state: FSMContext):
	answer = message.text
	await state.update_data(answer2=answer)# тут же он записывает наш ответ (наш линк)
	await message.answer('Дата в формате год-месяц-число, например 2023-04-05')
	await UserInfo.date.set()

# Обработка введённых значений
@dp.message_handler(state=UserInfo.date)# Текст пришел а значит переходим к этому шагу
async def answer_q3(message: types.Message, state: FSMContext):
	answer = message.text
	await state.update_data(answer3=answer)# опять же он записывает второй ответ

	# Ответы в переменную
	data = await state.get_data()
	answer1 = data.get("answer1")
	answer2 = data.get("answer2")
	answer3 = data.get("answer3")

	# Вывод введённых значений для проверки
	await message.answer("Город отправления: "+answer1+"\nГород прибытия: "+answer2+"\nДата поездки: "+answer3,reply_markup=greet_kb)


	AB = BashRoute(answer1, answer2, answer3)
	resAB = AB.WayResult()
	await message.answer(str(resAB[0]))
	for i in range(1,len(resAB)):
		mes = ""
		for j in range(len(resAB[i])):
			mes = mes + resAB[i][j] + "\n"	
		await message.answer(mes)
	#
	#
	#

	# Финальная стадия, очищает все данные из оперативной памяти
	await state.finish()

# Запуск процесса поллинга новых апдейтов
async def main():
	#Пропуск сообщений, которые приходили при неактиве бота
	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)

if __name__ == "__main__":
	asyncio.run(main())
