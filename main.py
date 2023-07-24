import os
import ast
import time
import json
import redis
from dotenv import load_dotenv

from redis_utils import get_channels_keys_and_values


def load_data_to_redis(filename, redis_client):
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.split("': ", 1)
            key = key[2:]

            value = ast.literal_eval(value.strip())
            value_json = json.dumps(value)

            redis_client.execute_command('JSON.SET', key, '.', value_json)


def wait_for_redis_ready(redis_client, max_retries=10, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            redis_client.ping()
            return True
        except redis.exceptions.BusyLoadingError:
            time.sleep(retry_interval)
            retries += 1
    return False


if __name__ == "__main__":
    # Загрузка переменных окружения из файла .env
    load_dotenv()

    # Получение данных для подключения к Redis из переменных окружения
    redis_host = os.getenv('REDIS_HOST')
    redis_port = int(os.getenv('REDIS_PORT'))
    redis_password = os.getenv('REDIS_PASSWORD')

    # Подключение к Redis
    redis_client = redis.StrictRedis(
        host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Ожидание, пока Redis станет доступен
    if wait_for_redis_ready(redis_client):
        # Загрузка данных из файла data.txt в Redis
        data_file = "data.txt"
        load_data_to_redis(data_file, redis_client)
        print("Данные успешно загружены в Redis.")
    else:
        print("Не удалось подключиться к Redis.")

    data = get_channels_keys_and_values(redis_client)

    print('Готово.')
