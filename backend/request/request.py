# Сторонние импорты
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

# Стандартный класс запроса
class Request():

	name = 'default'
	caption = 'default_question'
	error_message = 'default_error_message'
	markup = types.ReplyKeyboardRemove()

	def __init__(self):
		pass

	def load_request(self):
		# caption, markup, mode
		# Текст запроса
		self.name = 'default'
		self.caption = 'default_question'

	def set_value(self,value):
		self.value = value
		return True

	def get_reply_markup(self,list_of_button):
		markup = types.ReplyKeyboardMarkup(one_time_keyboard = True,
											resize_keyboard=True)
		for el in list_of_button:
			markup.row(*el)
		return markup

	def get_inline_markup(self,list_of_button,row_width = 1):
		markup = types.InlineKeyboardMarkup(one_time_keyboard = True,
											resize_keyboard=True,
											row_width = row_width)
		for el in list_of_button:
			button = types.InlineKeyboardButton(el, callback_data = el)
			markup.insert(button)
		return markup


class Request_factory(StatesGroup):

	state = State()

	def __init__(self, chat_id):
		# Установка этапа
		self.stage = -1
		# Создание выходного словаря
		self.result_dict = {}
		# Запись ID
		self.UID = str(chat_id)
		self.result_dict['UID'] = self.UID
		# Список запросов
		self.options()

	def options(self):
		self.list_of_request = []

	def get_next(self):
		# Повышаем stage
		self.stage += 1
		# возвращаем объект запроса
		if self.stage < (len(self.list_of_request)):
			self.list_of_request[self.stage].load_request()
			return self.list_of_request[self.stage]
		else:
			ending_mess = self.confirm()
			return ending_mess

	def set_value(self, value):
		# Добавляем значение в объект запроса
		value = value.replace('<','').replace('>','')
		status = self.list_of_request[self.stage].set_value(value)
		# Добавляем значение в словарь результатов
		if status == True:
			self.result_dict[self.list_of_request[self.stage].name] = self.list_of_request[self.stage].value
			return True
		else:
			error_message = self.list_of_request[self.stage].error_message
			self.stage -= 1
			return error_message

	def confirm(self):
		print(self.result_dict)
		return 'Тест закончен'



















