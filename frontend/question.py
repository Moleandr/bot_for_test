# Сторонние импорты
import logging
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import uuid
import os
# Локальные импорты
from backend import *


# Получаем ссылку на объект логгера
logger = logging.getLogger(__name__)

@dp.callback_query_handler(lambda call: call.data == "Принять участие")
async def query_q(call: types.CallbackQuery, state: FSMContext):
	# логирование
	logg_call(logger, call, await state.get_state())
	# бизнес
	factory = Test_factory(call.message.chat.id)
	await factory.state.set()
	await state.update_data(factory = factory)
	request = factory.get_next()
	# Обработка запроса
	try:
		await call.message.edit_reply_markup(reply_markup = None)
		await bot.send_message(call.message.chat.id, request.caption, reply_markup=request.markup)
	except:
		await bot.send_message(call.message.chat.id, request.caption)

@dp.callback_query_handler(state = Test_factory.state)
async def query_q(call: types.CallbackQuery, state: FSMContext):
	# логирование
	logg_call(logger, call, await state.get_state())
	# бизнес
	middle = await state.get_data()
	factory = middle['factory']
	status = factory.set_value(call.data)
	if status != True:
		await bot.send_message(call.chat.id, status)
	request = factory.get_next()
	await state.update_data(factory = factory)
	try:
		if request.mtype == 'text':
			await call.message.edit_text(request.caption, reply_markup=request.markup)
		if request.mtype == 'photo':
			await call.message.edit_reply_markup(reply_markup = None)
			try:
				await call.message.edit_caption(f'Ваша оценка: {call.data}')
			except:
				await call.message.delete()
			await bot.send_photo(call.message.chat.id, request.photo, reply_markup=request.markup)
	except:
		await call.message.edit_caption(f'Ваша оценка: {call.data}')
		await state.finish()
		await bot.send_message(call.message.chat.id,request)