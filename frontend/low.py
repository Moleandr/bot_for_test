# Сторонние импорты
import logging
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import filters
from aiogram.dispatcher import FSMContext
# Локальные импорты
from backend import *
from frontend.menu import menu

# Получаем ссылку на объект логгера
logger = logging.getLogger(__name__)


# Если совокупность команда/состояние неизвестно -> вызов меню
@dp.message_handler(content_types=types.ContentTypes.ANY,state = '*')
async def unknown_command(message: types.Message, state: FSMContext):
	# логирование
	logg_mess(logger, message, await state.get_state())
	#
	print("Функция низшего уровня в ответ на текстовое сообщение")
	await menu(message, state)


# Если совокупность команда/состояние неизвестно -> вызов меню
@dp.callback_query_handler(state = '*')
async def unknown_call(call, state: FSMContext):
	# логирование
	logg_call(logger, call, await state.get_state())
	#
	print("Функция низшего уровня в ответ на нажатие кнопки")
	await call.message.edit_reply_markup(reply_markup = None)
	await menu(call.message, state)