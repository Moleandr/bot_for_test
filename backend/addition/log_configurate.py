# Сторонние импорты
import logging
import logging.config
import emoji
import re
from aiogram.dispatcher.filters.state import State
import os

try:
    os.mkdir('logs')
except:
    pass

Config = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'default': {
                'format': '[%(asctime)s] (%(levelname).1s:%(name)s) %(message)s',
                # 'datefmt': '%Y/%m/%d %H:%M:%S.%f',
            },
        },

        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default',
            },
            'info_file':{
                'class': 'logging.FileHandler',
                'filename': 'logs/INFO.log',
                'level': 'INFO',
                'mode': 'w',
                'formatter': 'default',
            },
            'error_file':{
                'class': 'logging.FileHandler',
                'filename': 'logs/ERROR.log',
                'level': 'ERROR',
                'mode': 'w',
                'formatter': 'default',
            },
        },

        'root': {
            'level': 'DEBUG',
            'handlers': ['console','info_file','error_file'],
        },
    }

# Инициализация настроек логгера
logging.config.dictConfig(Config)
# Получаем ссылку на объект логгера
logger = logging.getLogger(__name__)

def my_decode(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Функция обработки логгером нажатия кнопки
def logg_call(logger,call,state):
	logger.info('id:' + str(call['from']['id']) + ' Text:' + str(call.data) + ' State:' + str(state))
# Функция обработки логгером текстового сообщения
def logg_mess(logger,message,state):
	logger.info('id:' + str(message['from']['id']) + ' Text:' + '********' + ' State:' + str(state))