import time
import asyncio

async def run_callback_for_one_minute(callback, duration):
    for _ in range(duration):
        await callback()  # Ожидаем выполнение асинхронного колбека
        await asyncio.sleep(1)  # Ожидание в 1 секунду

def call_callback_for_one_minute(callback):
    duration = 60  # Продолжительность в секундах (1 минута = 60 секунд)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_callback_for_one_minute(callback, duration))

# Пример функции-колбека
# def my_callback():
#     print("Вызван колбек!")


# Вызываем функцию, передавая ей колбек и продолжительность
# call_callback_for_one_minute(my_callback)