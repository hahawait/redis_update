import redis
import json


def get_json_data(key, redis_client):
    data = redis_client.execute_command('JSON.GET', key)
    return json.loads(data)


def get_channels_keys_and_values(redis_client):
    key_pattern = "channels:*:users:*"
    channels_keys = redis_client.keys(key_pattern)

    channels_values = [get_json_data(key, redis_client)
                       for key in channels_keys]

    channels_data = list(zip(channels_keys, channels_values))

    return channels_data
