# Сторонние импорты
import logging
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
# Локальные импорты
from backend import *


# Получаем ссылку на объект логгера
logger = logging.getLogger(__name__)


# Главное меню
@dp.message_handler(commands=['menu', 'start'], state = '*')
async def menu(message: types.Message, state: FSMContext):
	# логирование
	logg_mess(logger, message, await state.get_state())
	# Работа с состоянием
	await state.finish()
	text = '''
Привет! Мы - команда разработчиков из Самарского университита. 
Наша идея: создать нейросеть, которая будет рекомендовать пользователю приложения или сайты, на основе индивидуально-психологических черт личности.
Для обучения нам необходимо собрать некоторое количество "живых" ответов.
Мы будем тебе очень благодарны, если ты примешь участие в тесте.
'''
	markup = Markup.inline_markup_from_list(['Принять участие'])
	await bot.send_message(message['chat']['id'],text = text,reply_markup = markup)
