import logging
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import text, bold, italic, code, pre  # markdown utils
from aiogram.types import ParseMode as PM  # to send text in markdown

from dict import lessons_top, lessons_down, lsn_emoji, lsn_time

# Initialize bot and dispatcher
bot = Bot(token='***REMOVED***')
dp = Dispatcher(bot, storage=MemoryStorage())

# Configure logging
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
					level=logging.DEBUG, filename="schedule.log")

dp.middleware.setup(LoggingMiddleware())

ADMIN_ID = [***REMOVED***]


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

	inline_keyboard.add(InlineKeyboardButton('♻️ Змінити тиждень', callback_data='refresh'))

	return inline_keyboard


def generate_schedule(day, top):  # 0, True
	schedule = '📋 ' + bold('Розклад для ФЛО-41') + '\n🔸 Поточний по '

	if int((datetime.date.today() - datetime.date(2020, 3, 2)).days / 7) % 2 == 0:
		schedule += 'чисельнику\n🔹 Розклад для '
	else:
		schedule += 'знаменнику\n🔹 Розклад для '

	if top_week:
		schedule += 'чисельника\n\n'
	else:
		schedule += 'знаменника\n\n'

	was = False
	if top:
		lessons = lessons_top
	else:
		lessons = lessons_down

	for i in range(8):
		if not len(lessons[day][i]) == 0:
			if was:
				schedule += '\n➖➖➖➖➖➖➖➖➖➖\n'
			else:
				was = True
			schedule += lsn_emoji[i] + " " + bold(lessons[day][i]['name']) + '\n🎓 ' + lessons[day][i]['teacher']
			schedule += '\n📍 ' + lessons[day][i]['room'] + ', ' + lessons[day][i]['type'] + '\n🕓  ' + lsn_time[i]

	return schedule


def set_week():
	"""Повертає чи зараз тиждень по чисельнику"""
	global top_week  # True — чисельник, False — знаменник
	start_week = datetime.date(2020, 3, 2)  # тиждень числельника
	current_week = datetime.date.today()
	if int((current_week - start_week).days / 7) % 2 == 0:
		top_week = True
	else:
		top_week = False


def swap_week():
	"""Змінює тиждень на інший по чисельнику/знаменику"""
	global top_week  # True — чисельник, False — знаменник

	if top_week:
		top_week = False
	else:
		top_week = True


def get_day():
	"""Повертає день тижня -1"""
	return datetime.datetime.today().weekday()


@dp.message_handler(commands=['start'])
async def start_function(message: types.Message):
	"""При старті, воно закріплює внизу кнопку"""
	start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('🎓 Розклад занять'))
	await bot.send_message(message.from_user.id, "Привіт! Тисни кнопку і дивись розклад 👇",
						   reply_markup=start_keyboard)


@dp.message_handler(text='🎓 Розклад занять')
async def schedule_function(message: types.Message):
	"""Опис"""
	set_week()
	await bot.send_message(message.from_user.id, generate_schedule(get_day(), top_week), parse_mode=PM.MARKDOWN,
						   reply_markup=create_inline_keyboard(get_day()))


@dp.callback_query_handler(text='monday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(0, top_week), chat_id=query.from_user.id,
								message_id=query.message.message_id, parse_mode=PM.MARKDOWN,
								reply_markup=create_inline_keyboard(0))


@dp.callback_query_handler(text='tuesday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(1, top_week), chat_id=query.from_user.id,
								message_id=query.message.message_id, parse_mode=PM.MARKDOWN,
								reply_markup=create_inline_keyboard(1))


@dp.callback_query_handler(text='wednesday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(2, top_week), chat_id=query.from_user.id,
								message_id=query.message.message_id, parse_mode=PM.MARKDOWN,
								reply_markup=create_inline_keyboard(2))


@dp.callback_query_handler(text='thursday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(3, top_week), chat_id=query.from_user.id,
								message_id=query.message.message_id, parse_mode=PM.MARKDOWN,
								reply_markup=create_inline_keyboard(3))


@dp.callback_query_handler(text='friday')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	await bot.edit_message_text(text=generate_schedule(4, top_week), chat_id=query.from_user.id,
								message_id=query.message.message_id, parse_mode=PM.MARKDOWN,
								reply_markup=create_inline_keyboard(4))


@dp.callback_query_handler(text='refresh')
async def refresh_callback_handler(query: types.CallbackQuery):
	await query.answer('😉')
	swap_week()
	await bot.edit_message_text(text=generate_schedule(get_day(), top_week), chat_id=query.from_user.id,
								message_id=query.message.message_id, parse_mode=PM.MARKDOWN,
								reply_markup=create_inline_keyboard(get_day()))


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


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
