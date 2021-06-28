from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# Расшарить таблицу для сервисного аккаунта
# account@third-arcadia-293114.iam.gserviceaccount.com

# Очень стыдный костыль
dict_of_translate = {
	"1":"A",
	"2":"B",
	"3":"C",
	"4":"D",
	"5":"E",
	"6":"F",
	"7":"G",
	"8":"H",
	"9":"I",
	"10":"J",
	"11":"K",
	"12":"L",
	"13":"M",
	"14":"N",
	"15":"O",
	"16":"P",
	"17":"Q",
	"18":"R",
	"19":"S",
	"20":"T",
	"21":"U",
	"22":"V",
	"23":"W",
	"24":"X",
	"25":"Y",
	"26":"Z",
}

# Стоит ограничение по столбцам до Z

CREDENTIALS_FILE = 'creds.json'

class Sheet(object):

	def __init__(self, spreadsheet_id):
		# Авторизуемся и получаем service — экземпляр доступа к API
		credentials = ServiceAccountCredentials.from_json_keyfile_name(
		    CREDENTIALS_FILE,
		    ['https://www.googleapis.com/auth/spreadsheets',
		     'https://www.googleapis.com/auth/drive'])
		httpAuth = credentials.authorize(httplib2.Http())
		self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
		self.spreadsheet_id = spreadsheet_id

	# Получить значения по имени ячейки
	def get_value(self, name):
		# Реализуем запрос
		value = self.service.spreadsheets().values().get(
		    spreadsheetId=self.spreadsheet_id,
		    range=name,
		    majorDimension='COLUMNS'
		).execute()
		# Форматируем ответ
		return value['values'][0][0]
		
	# Получить значения ячеек в диапазоне
	def get_values(self, range_name, majorDimension = 'ROWS'):   # ROWS/COLUMNS
		# Реализуем запрос
		value = self.service.spreadsheets().values().get(
		    spreadsheetId=self.spreadsheet_id,
		    range=range_name,
		    majorDimension=majorDimension
		).execute()
		# Форматируем ответ
		return value['values']

	# Записать значение в ячейку
	def write_value(self, name, value):
		self.service.spreadsheets().values().batchUpdate(
		    spreadsheetId=self.spreadsheet_id,
		    body={
		        "valueInputOption": "USER_ENTERED",
		        "data":
		            {"range": name,
		             "majorDimension": "ROWS",
		             "values": [[value]]},
		    }
		).execute()

	# Записать пул значений в таблицу
	def write_values(self, range_name, value, majorDimension = 'ROWS'): # ROWS/COLUMNS
		self.service.spreadsheets().values().batchUpdate(
		    spreadsheetId=self.spreadsheet_id,
		    body={
		        "valueInputOption": "USER_ENTERED",
		        "data":
		            {"range": range_name,
		             "majorDimension": majorDimension,
		             "values": value},
		    }
		).execute()

	def get_sheet_id(self, name):
		spreadsheet = self.service.spreadsheets().get(spreadsheetId = self.spreadsheet_id).execute()
		sheetList = spreadsheet.get('sheets')
		sheets = {}
		for el in sheetList:
			sheets[el['properties']['title']] = el['properties']['sheetId']
		return sheets[name]



	# Добавить чек-бокс в ячейку
	def add_checkbox(self, name, num_str, num_col):
		# 
		self.service.spreadsheets().batchUpdate(
			spreadsheetId=self.spreadsheet_id,
			body={
				'requests': [
					{'repeatCell':
							{
								'cell': {'dataValidation': {'condition': {'type': 'BOOLEAN'}}},
								'range': {'sheetId': self.get_sheet_id(name), 
									'startRowIndex': num_str-1, 
									'endRowIndex': num_str,
									'startColumnIndex': num_col-1,
									'endColumnIndex': num_col},
								'fields': 'dataValidation'
							}
					},
				]
		}).execute()


	# Добавить новую строку в конец (Возвращает номер ячейки в которую вставила)
	def add_record(self, range_name, values):
		res = self.service.spreadsheets().values().append(
		    spreadsheetId=self.spreadsheet_id,
		    range = range_name,
		    valueInputOption="USER_ENTERED",
		    body={"values": [values]}
		).execute()
		return res['updates']['updatedRange']

	def smart_add_record(self, sheet_name, dict_of_values):
		record = []
		# Получаем параметры шапки таблицы
		name_of_columns = self.get_values(sheet_name+"!1:1")[0]
		# Формируем выходной массив
		for name in name_of_columns:
			if name in dict_of_values:
				record.append(dict_of_values[name])
			else:
				record.append("")
		num = self.add_record(sheet_name+"!A2",record)
		return int(num.split('!')[1].split(':')[0][1:])

	def get_unic_values_in_column(self, sheet_name, name_of_column):
		massive = []
		# забираем всю таблицу
		table = self.get_values(sheet_name+"!A1:Z", 'COLUMNS')
		for column in table:
			if column[0] == name_of_column:
				massive = column[1:]
		massive = list(set(massive))
		return massive

	# Функция позволяющая получить значение столбцов в таблице отфильтрованных по какому-то признаку
	def get_records_with_filter(self, sheet_name, filter_name, filter_value, columns_name):
		result_massive = []
		# забираем всю таблицу
		table = self.get_values(sheet_name+"!A1:Z", 'ROWS')
		# Находим позицию столбика-фильтра
		num_of_filter_column = table[0].index(filter_name)
		# Определяем массив позиций необходимых при выдаче
		mass_of_names = []
		for name in columns_name:
			position = table[0].index(name)
			mass_of_names.append([name,position])
		# Ищем записи, добавляем в результат
		for row in table:
			if row[num_of_filter_column] == filter_value:
				row_dict = {}
				for mass_of_col in mass_of_names:
					row_dict[mass_of_col[0]] = row[mass_of_col[1]]
				result_massive.append(row_dict)
		return result_massive

	# Получение записи по ПК
	def get_record_from_ID(self, sheet_name, key_column, key_value):
		result_dict = {}
		# забираем всю таблицу
		table = self.get_values(sheet_name+"!A1:Z", 'ROWS')
		# Находим позицию столбика-первичного ключа
		num_of_key_column = table[0].index(key_column)
		finding_row = []
		# Ищем строку
		try:
			for row in table:
				if row[num_of_key_column] == key_value:
					finding_row = row
			# Формируем выходной словарь
			for i in range(0,len(table[0])):
				result_dict[table[0][i]] = str(finding_row[i])
			return result_dict
		except:
			return None

	def get_next_ID(self, sheet_name):
		# забираем первый столбец
		table = self.get_values(sheet_name+"!A1:A", 'ROWS')
		# Берём Id последней записи
		last_ID = table[-1][0]
		try:
			ID = str(int(last_ID)+1)
		except:
			ID = 1
		return ID

	def update_value_in_record(self, sheet_name, ID, edit_column, edit_value):
		# Ищем координаты для замещения
		# забираем первую строку
		first_row = self.get_values(sheet_name+"!A1:Z1", 'ROWS')
		# первый стобец
		first_column = self.get_values(sheet_name+"!A1:A", 'COLUMNS')
		#
		# Ищем строку
		changing_row = first_column[0].index(ID)+1
		# Ищем столбец
		changing_column = first_row[0].index(edit_column)+1
		# перводим в букву
		changing_column = dict_of_translate[str(changing_column)]
		self.write_value(sheet_name+"!"+str(changing_column)+str(changing_row), edit_value)




# sheet = Sheet('1Jo9okycXRhAS12__O0cVlCMV53VJPEsPondUEZcMblg')
# sheet.add_checkbox('Пользователи', 10, 5)








