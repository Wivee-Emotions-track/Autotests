import json
import requests
import os
from os import path

ENV = 'staging1'

BROWSERS = {
    "chromium": ["latest"],
    "firefox": ["latest"],
    "webkit": ["latest"]
}


def get_env_configs(env):

    config_path = path.join(path.dirname(__file__), "env_configs.json")
    if not os.path.exists(config_path):
        save_env_configs(env)
    with open(config_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        return data


def save_env_configs(env):
    config_path = path.join(path.dirname(__file__), "env_configs.json")
    data = get_data_from_vault()
    config_dict = {"urls": data['contour_url'].get(env, 'No configs for this contour'),
                   "credentials": data.get("credentials")
                   }
    with open(config_path, "w") as file:
        json.dump(config_dict, file, indent=4)


def get_env():

    if os.getenv("ENV"):
        return os.getenv("ENV")
    else:
        return ENV


def get_data_from_vault():

    vault_address = 'https://vault.wayvee.com/v1/cubbyhole/autotests_secrets'

    vault_token = os.getenv('VAULT_TOKEN')

    headers = {
        "X-Vault-Token": vault_token
    }

    response = requests.get(vault_address, headers=headers)
    return response.json()['data']
