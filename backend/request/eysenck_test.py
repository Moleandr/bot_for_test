from backend.request.request import Request, Request_factory
from aiogram.dispatcher.filters.state import State
from datetime import datetime
import pandas as pd
from pprint import pprint

import backend
from re import *

file_path = 'Вопросы.csv'

photo_id = [
	['1','AgACAgIAAxkBAAMhYNhVxb2Pon4-0dTens7Ye71vq5kAAoS0MRuV3cFK73Vhw1XuLlQBAAMCAANzAAMgBA'],
	['2','AgACAgIAAxkBAAMiYNhWOVdxLzV1dH99KaxI_XHD75sAAoa0MRuV3cFKAsTgBWtVQRABAAMCAANzAAMgBA'],
	['3','AgACAgIAAxkBAAMjYNhWfEGepoXSZV4Jw4dOxd2xiFwAAoe0MRuV3cFKkFpJZK_U7rcBAAMCAANzAAMgBA'],
	['4','AgACAgIAAxkBAAMkYNhWtvXUQZuC9WaMNkTUlQZivuwAAom0MRuV3cFKjaVJbO8kH5QBAAMCAANzAAMgBA'],
	['5','AgACAgIAAxkBAAMlYNhW1O9-ULyLZ38xvArVG1ZA7gcAAoq0MRuV3cFKM7Jd4DGrMr4BAAMCAANzAAMgBA'],
	['6','AgACAgIAAxkBAAMmYNhXKtt-8w7Vi2dy15Skfxm357QAAo20MRuV3cFKyz25ZXDn_wkBAAMCAANzAAMgBA'],
	['7','AgACAgIAAxkBAAMnYNhXfMd1HNhTE4texy09b8xkKD0AAo60MRuV3cFK5kR5WH_4pc4BAAMCAANzAAMgBA'],
	['8','AgACAgIAAxkBAAMoYNhXnWedZ8AEvr93nrVwd1eDUsIAApC0MRuV3cFKd5UAAUlHVuvQAQADAgADcwADIAQ']
]

mass_of_question = pd.read_csv(file_path,';').values.tolist()

keys = {'психотизм':{'yes':['14', '23', '27', '31', '35', '47', '51', '55', '71', '85', '88', '93', '97'],
				'no':['2', '6', '9', '11', '19', '39', '43', '59', '63', '67', '78', '100']
				},
		'экстраверсия-интроверсия':{'yes':['1', '5', '10', '15', '18', '26', '34', '38', '42', '50', '54', '58', '62', '66', '70', '74', '77', '81', '90', '92', '96'],
				'no':['22', '30', '46', '84']
				},
		'нейтротизм':{'yes':['3', '7', '12', '16', '20', '24', '28', '32', '36', '40', '44', '48', '52', '56', '60', '64', '68', '72', '75', '79', '83',
'86', '89', '94', '98'],
				'no':[]
				},
		'искренность':{'yes':['13', '21', '33', '37', '61', '73', '87', '99'],
				'no':['4', '8,' '17', '25', '29', '41', '45', '49', '53', '57', '65', '69', '76', '80', '82', '91', '95']
				},
		}

def decrypt_yes(result,dec_mass):
	sum = 0
	for el in dec_mass:
		if el in result:
			sum += int(result[el])
	return sum

def decrypt_no(result,dec_mass):
	sum = 0
	for el in dec_mass:
		if el in result:
			sum += not(int(result[el]))
	return sum

def decrypt(result, keys):
	result_dict = {}
	for group in keys:
		sum = 0
		sum += decrypt_yes(result,keys[group]['yes'])
		sum += decrypt_no(result,keys[group]['no'])
		result_dict[group] = sum
	return result_dict

class Begin1(Request):

	def load_request(self):
		self.mtype = 'text'
		self.name = 'begin1'
		self.caption = '''
Тебе предлагается ответить на вопросы, касающиеся твоего обычного
способа поведения. Постарайся представить типичные ситуации и дай первый
«естественный» ответ, который придет в голову.'''
		self.markup = self.get_inline_markup(['Начать тестирование'])

class Begin2(Request):

	def load_request(self):
		self.mtype = 'text'
		self.name = 'begin2'
		self.caption = '''
Сейчас тебе будет показан ряд сайтов, для каждого из которых необходимо выбрать оценку от 1 до 10.'''
		self.markup = self.get_inline_markup(['Понятно'])

class Test_question(Request):

	def __init__(self, question):
		self.question = question

	def load_request(self):
		self.mtype = 'text'
		self.name = str(self.question[0])
		self.caption = str(self.question[0]) + '.' + self.question[1]
		self.markup = self.get_inline_markup(['Да', 'Нет'])

	def set_value(self, value):
		if value == 'Да':
			self.value = 1
		else:
			self.value = 0
		return True

class Photo_question(Request):

	def __init__(self, question):
		self.question = question

	def load_request(self):
		self.mtype = 'photo'
		self.name = 'website №' + self.question[0]
		self.photo = self.question[1]
		self.markup = self.get_inline_markup(['1', '2','3','4','5','6','7','8','9','10'],5)

	def set_value(self, value):
		if value.isdigit():
			self.value = value
			return True
		else:
			return False


class Test_factory(Request_factory):

	state = State()

	def options(self):
		self.list_of_request = [
			Begin1(),
			*[Test_question(el) for el in mass_of_question],
			Begin2(),
			*[Photo_question(el) for el in photo_id]
			]

	def confirm(self):
		self.result_dict['Дата'] = str(datetime.now())
		backend.sheet.smart_add_record('Ответы', self.result_dict)
		rez = decrypt(self.result_dict, keys)
		text = f'''
Спасибо за участие!
Ваши результаты:
Психотизм: {rez['психотизм']},
Экстраверсия-интроверсия: {rez['экстраверсия-интроверсия']},
Нейтротизм: {rez['нейтротизм']},
Искренность: {rez['искренность']}.
Если тебе интересно расшифровать свой результат и подробнее узнать про тест, можешь заглянуть http://onu.edu.ua/pub/bank/userfiles/files/rgf/rgf_metodiki.pdf
'''
		return text
