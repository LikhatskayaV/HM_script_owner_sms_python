import time
import threading
import requests
import random
import uuid
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine,text
from test_2 import call_callback_for_one_minute
import asyncio

# Создаем глобальную переменную для хранения значения amount_value
amount_value = None

# Создаем глобальную переменную для хранения значения card
card = None

# Получение текущего времени
current_time = datetime.now()
# Извлечение только времени без даты, секунд и миллисекунд
current_time_only = current_time.strftime('%H:%M')

# АПИ токен EPAY_TEST
bearer_token = "04|jtBAgWbTj6BkFZmLX1ZNtQPpY05t6eHzwLdr3lSh0AmyQhGKu2g4rX72y"



# Генерация случайного числа в диапазоне
random_amount = random.randint(100, 2000)

# Создание входящей заявки (Сбербанк)
api_url = "https://websitewizard.ru/api/v2/order/in"

# Заголовок Authorization с Bearer-токеном
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

# Выбор случайным образом одного из двух значений: 1 или 53
# random_bank = random.choice([1, 53])

# Подключение к базе данных
db_connection = "mysql"
db_host = "rc1a-abm0q3dtm870unzz.mdb.yandexcloud.net"
db_port = 3306
db_database = "dev_payment_system"
db_username = "mpoliakov"
db_password = "nq7cernm6mGU"

# Путь к SSL-сертификату root.crt (локальный путь)
ssl_cert_path = "C:/Users/yvasi/Downloads/Telegram Desktop/root.crt"

# Создание URL-адреса подключения с SSL-сертификатом
db_url = f"{db_connection}://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}?ssl_ca={ssl_cert_path}"

engine = create_engine(db_url)

# # Флаг для определения, какую функцию выполнить
# execute_api_request = True

# Функция для отправки запросов к API
def send_api_requests():
    global random_amount, amount_value, card, execute_api_request
    total_requests = 1
    requests_per_second = 1
    duration = 60 # 10 минут в секундах
    print("requests_per_second * duration >>>  ", requests_per_second * duration)
    print("total_requests >>> ", total_requests)
    while total_requests < (requests_per_second * duration):
        print("while >>>>")
        start_time = time.time()
        # Преобразование GUID в строку
        guid_str = str(uuid.uuid4())
        random_bank = random.choice([1, 53])
        headers = {
            "Authorization": f"Bearer {bearer_token}"
        }
        request_data = {
            "transactionId": guid_str,  # Уникальный ID запроса
            "amount": random_amount,  # Ваша сумма
            "bank": 1,
            "customerName": f"Evgeniy Automation{random_amount}",
            "customerIp": "123.456.789.0",
            "customerUserId": f"{random_amount}",
            "currencyCode": "RUB"
        }
        # Получение значения 'amount' из словаря request_data
        amount_value = request_data.get('amount')

        response = requests.post(api_url, headers=headers, json=request_data)

        print("response >>>> ", response.json());
        if response.status_code == 200:
            print("Запрос успешно отправлен >>> ",amount_value)
            execute_database_queries(amount_value)
        else:
            print(f"Ошибка при отправке запроса. Код статуса: {response.status_code}")
        print("do total_requests")
        total_requests += 1
        print("total_requests2 >>>>> ", total_requests)
        elapsed_time = time.time() - start_time
        time_to_sleep = 1 / requests_per_second - elapsed_time

        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

        # Переопределим random_amount для следующей итерации
        random_amount = random.randint(100, 2000)

        # Устанавливаем флаг для выполнения другой функции
        # execute_api_request = False

# Функция для выполнения SQL-запросов к базе данных
def execute_database_queries(value):
    global random_amount, amount_value, card, execute_api_request
    duration = 600
    print("test execute_database_queries >>>", value)
    start_time = time.time()
    # while time.time() - start_time < duration:
        # if execute_api_request:
            # Здесь добавляем код для выполнения SQL-запроса к базе данных
    connection = engine.connect()

    sql_query = text(f"SELECT owner_id, amount, card FROM tmp_active_orders tao WHERE amount = {amount_value}")

    result = connection.execute(sql_query)

    for row in result:
        owner_id = row.owner_id
        amount = row.amount
        card = row.card
        print(f"Owner ID: {owner_id}, Amount: {amount}, Card: {card} ")

        sql_query_raotg = text(f"SELECT name, channel_id FROM reg_agent_owners_tbl_goips raotg WHERE owner_id = {owner_id}")

        result_raotg = connection.execute(sql_query_raotg)

        for row_raotg in result_raotg:
            name = row_raotg.name
            channel_id = row_raotg.channel_id

            combined_info = f"{name}{channel_id}"
            print(f"Additional Info: {combined_info}")

            url_goip_check_sms = "https://websitewizard.ru/api/goip/checkSms"

            card_last_4_digits = card[-4:]

            json_data_goip_check_sms = {
                "goip_line": combined_info,
                "content": f" - MIR-{card_last_4_digits} {current_time_only} зачисление {amount_value}р Баланс: {364857.00 + amount_value}р[notification]"
            }

            response_goip_check_sms = requests.post(url_goip_check_sms, json=json_data_goip_check_sms)

            if response_goip_check_sms.status_code == 200:
                response_data_goip_check_sms = response_goip_check_sms.json()
                print(response_data_goip_check_sms)
            else:
                print(f"Ошибка при отправке POST-запроса в goip/checkSms. Код статуса: {response_goip_check_sms.status_code}")

            connection.close()

            # Добавим задержку перед следующим запросом
            # time.sleep()  # Задержка в 1 секунду между запросами

            # Устанавливаем флаг для выполнения другой функции
            # execute_api_request = False
# def send_requests():
#     start_time = time.time()
#     # Преобразование GUID в строку
#     guid_str = str(uuid.uuid4())
#     random_bank = random.choice([1, 53])
#     headers = {
#         "Authorization": f"Bearer {bearer_token}"
#     }
#     request_data = {
#         "transactionId": guid_str,  # Уникальный ID запроса
#         "amount": random_amount,  # Ваша сумма
#         "bank": random_bank,
#         "customerName": f"Evgeniy Automation{random_amount}",
#         "customerIp": "123.456.789.0",
#         "customerUserId": "123",
#         "currencyCode": "RUB"
#     }
#     # Получение значения 'amount' из словаря request_data
#     amount_value = request_data.get('amount')
#
#     return requests.post(api_url, headers=headers, json=request_data)
#     pass

# async def main_test():
#     results = await asyncio.gather(
#         send_requests(), send_requests(), send_requests(), send_requests(), send_requests()
#     )
#     print(results)
#
#
# if __name__ == "__main__":
#     call_callback_for_one_minute(main_test)

if __name__ == "__main__":
    api_thread = threading.Thread(target=send_api_requests)

    api_thread.start()


    api_thread.join()