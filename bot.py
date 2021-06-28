# Сторонние импорты
import logging
from aiogram import executor
# Локальные импорты
import backend
import frontend

# Получаем ссылку на объект логгера
logger = logging.getLogger(__name__)


if __name__ == "__main__":
	try:
		executor.start_polling(backend.dp)
	except Exception as e:
		logger.error(e, exc_info=True)