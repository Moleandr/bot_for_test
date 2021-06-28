from aiogram import types


# Функция создания обычной клавиатуры из массива
def markup_from_list(massive):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard = True,resize_keyboard=True)
	for el in massive:
		button = types.KeyboardButton(el)
		markup.add(button)
	return markup

# Функция создания инлайн клавиатуры из массива
def inline_markup_from_list(massive = [], additional_buttons_name = [], additional_buttons_data = [], row_width = 1):
	# создаём клавиатуру
	markup = types.InlineKeyboardMarkup(one_time_keyboard = True,resize_keyboard=True, row_width = row_width)
	# создание клавиатуры из массива
	for el in massive:
		button = types.InlineKeyboardButton(el, callback_data = el)
		markup.insert(button)
	# дополнительная кнопка (вне ряда)
	if additional_buttons_name != []:
		for el1,el2 in zip(additional_buttons_name,additional_buttons_data):
			button = types.InlineKeyboardButton(el1, callback_data = '*' + el2)  # call.data начинается со звёздочки
			markup.add(button)
	return markup