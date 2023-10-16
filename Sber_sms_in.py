import requests
import json
import uuid
import random
import time
from sqlalchemy import create_engine, text
from datetime import datetime

# Получите текущее время
current_time = datetime.now()

# Извлечение только времени без даты, секунд и миллисекунд
current_time_only = current_time.strftime('%H:%M')

# АПИ токен EPAY_TEST
bearer_token = "04|jtBAgWbTj6BkFZmLX1ZNtQPpY05t6eHzwLdr3lSh0AmyQhGKu2g4rX72y"

# Генерируем новый GUID
new_guid = uuid.uuid4()

# Преобразуем GUID в строку
guid_str = str(new_guid)

# Генерация случайного числа в диапазоне
random_amount = random.randint(100, 2000)

# Выбор случайным образом одного из двух значений: 1 или 53
random_bank = random.choice([1, 53])
# Создание входящей заявки (Сбербанк)
api_url = "https://websitewizard.ru/api/v2/order/in"

# Заголовок Authorization с Bearer-токеном
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

# Создаем тела запроса в формате JSON
request_data = {
    "transactionId": guid_str,
    "amount": random_amount,
    "bank": 1,
    "customerName": f"Evgeniy Automation{random_amount}",
    "customerIp": "2202200223948484",
    "customerUserId": "264",
    "currencyCode": "RUB"
}
# Получем значение 'amount' из словаря request_data
amount_value = request_data.get('amount')

# Отправляем POST-запроса
response = requests.post(api_url, headers=headers, json=request_data)

# Проверка статуса ответа
if response.status_code == 200:
    # Распарсивание JSON-ответа
    response_json = response.json()
else:
    print(f"Ошибка при отправке запроса. Код статуса: {response.status_code}")



# Подключаемся к базе данных
db_connection = "mysql"
db_host = "rc1a-abm0q3dtm870unzz.mdb.yandexcloud.net"
db_port = 3306
db_database = "dev_payment_system"
db_username = "mpoliakov"
db_password = "nq7cernm6mGU"

# Путь к SSL-сертификату root.crt (локальный путь)
ssl_cert_path = "C:/Users/yvasi/Downloads/Telegram Desktop/root.crt"

# Создайем URL-адрес подключения с SSL-сертификатом
db_url = f"{db_connection}://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}?ssl_ca={ssl_cert_path}"

engine = create_engine(db_url)

# Создаем соединение
connection = engine.connect()

# Создаем SQL-запрос, вставив значение amount_value в строку запроса
sql_query = text(f"SELECT owner_id, amount, card FROM tmp_active_orders tao WHERE amount = {amount_value}")

# Выполняем SQL-запрос
result = connection.execute(sql_query)

# Обработаем результаты запроса
for row in result:
    owner_id = row.owner_id
    amount = row.amount
    card = row.card
    print(f"Owner ID: {owner_id}, Amount: {amount}, Card: {card} ")

# Второй SQL-запрос, используем значение owner_id из первого запроса
    sql_query_rao = text(f"SELECT owner_id, imei FROM reg_agent_owners rao WHERE owner_id = {owner_id}")

# Выполните второй SQL-запрос
    result_rao = connection.execute(sql_query_rao)

# Обработаем результаты второго запроса
    for row_rao in result_rao:
        owner_id_rao = row_rao.owner_id
        imei = row_rao.imei

        print(f"Owner ID (RAO): {owner_id_rao}, IMEI: {imei}")

# Закрываем соединение
connection.close()

time.sleep(1)

# Парсинг смс
# Получаем значение 'imei' из результатов второго запроса
imei_value = imei

# Получаем значение 'card_last_4_digits' из результатов первого запроса
card_last_4_digits = card[-4:]

print(card_last_4_digits)
# Формируем текст для запроса
text = f"- MIR-{card_last_4_digits} {current_time_only} зачисление {amount_value}р Баланс: 200000р[notification]"

# Создаем URL для GET-запроса
url = f"https://websitewizard.ru/api/macrodroid/checkSms?imei={imei_value}&text={text}"

# Отправляем GET-запрос
response = requests.get(url)

# Проверяем статус ответа
if response.status_code == 200:
    response_data = response.json()
    print(response_data)
else:
    print(f"Ошибка при отправке GET-запроса. Код статуса: {response.status_code}")