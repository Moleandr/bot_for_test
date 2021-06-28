# Сторонние импорты
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# Локальные импорты
from backend import config
from backend.addition.sheets_editor import Sheet

# Создаём объекты бота
bot = Bot(config.TOKEN, parse_mode=types.ParseMode.HTML)
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)

# Объект таблицы
sheet = Sheet('1lHSSIMuOIEPsv_1Ots3XIelX-dH3V8jUDwb40FOkHFc')

