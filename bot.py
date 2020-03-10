import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import text, bold, italic, code, pre  # markdown utils
from aiogram.types import ParseMode as PM  # to send text in markdown
from lessons import lessons_top, lessons_down

# Initialize bot and dispatcher
bot = Bot(token='***REMOVED***')
dp = Dispatcher(bot, storage=MemoryStorage())

# Configure logging
# logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
# 					level=logging.DEBUG, filename="schedule.log")

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
					level=logging.INFO)

dp.middleware.setup(LoggingMiddleware())

ADMIN_ID = [***REMOVED***]


async def check_admin(message):
	"""Обмежує використання функції тільки для адміна"""
	if message.from_user.id not in ADMIN_ID:
		report = 'name: ' + str(message.from_user.full_name) + '\n'
		if message.from_user.username:
			report += 'username: ' + str(message.from_user.username) + '\n'
		report += 'id: ' + str(message.from_user.id) + '\n'
		report += 'chat: ' + str(message.chat.type)
		await bot.send_message(ADMIN_ID[0], report)
		raise Exception('not admin')


@dp.message_handler(commands=['log'])
async def log_function(message: types.Message):
	"""Отримати лог"""
	await check_admin(message)
	with open('schedule.log', 'r') as logfile:
		await message.answer_document(logfile, reply=False)


@dp.message_handler(commands=['delog'])
async def clear_log_function(message: types.Message):
	"""Очистити лог"""
	await check_admin(message)
	with open('schedule.log', 'w') as logfile:
		pass
	await message.reply('cleared ;)', reply=False)


def create_inline_keyboard(day):
	inline_keyboard = InlineKeyboardMarkup()

	btns = []
	days_ukr = ['пн', 'вт', 'ср', 'чт', 'пт']
	days_query = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
	for i in range(5):
		if i == day:
			this_button = InlineKeyboardButton('➡️ ' + days_ukr[i], callback_data=days_query[i])
		else:
			this_button = InlineKeyboardButton(days_ukr[i], callback_data=days_query[i])
		btns.append(this_button)
	inline_keyboard.row(*btns)

	return inline_keyboard


def generate_schedule(day):
	schedule = ''
	schedule += 'Текст'
	return schedule


@dp.message_handler(commands=['start'])
async def start_function(message: types.Message):
	"""Опис"""

	start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('🎓 Розклад занять'))
	await bot.send_message(message.from_user.id, generate_schedule(0), parse_mode=PM.MARKDOWN,
						   reply_markup=start_kb)


@dp.message_handler(text='🎓 Розклад занять')
async def schedule_function(message: types.Message):
	"""Опис"""

	# TODO: доробити момент, щоб воно визначало який сг день і видавало розклад на цей день

	# TODO: доробити момент, щоб воно розуміло сг знаменник чи чисельник

	await bot.send_message(message.from_user.id, generate_schedule(0), parse_mode=PM.MARKDOWN,
						   reply_markup=create_inline_keyboard(0))


@dp.callback_query_handler(text='monday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(0), chat_id=query.from_user.id,
								message_id=query.message.message_id, reply_markup=create_inline_keyboard(0))


@dp.callback_query_handler(text='tuesday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(1), chat_id=query.from_user.id,
								message_id=query.message.message_id, reply_markup=create_inline_keyboard(1))


@dp.callback_query_handler(text='wednesday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(2), chat_id=query.from_user.id,
								message_id=query.message.message_id, reply_markup=create_inline_keyboard(2))


@dp.callback_query_handler(text='thursday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(3), chat_id=query.from_user.id,
								message_id=query.message.message_id, reply_markup=create_inline_keyboard(3))


@dp.callback_query_handler(text='friday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(4), chat_id=query.from_user.id,
								message_id=query.message.message_id, reply_markup=create_inline_keyboard(4))


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
