import json
import requests
import os
from os import path

ENV = None

BROWSERS = {
    "chromium": ["latest"],
    "firefox": ["latest"],
    "webkit": ["latest"]
}


def get_env_configs():

    config_path = path.join(path.dirname(__file__), "env_configs.json")
    if not os.path.exists(config_path):
        save_env_configs(get_env())
    with open(config_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        return data


def save_env_configs(env):
    config_path = path.join(path.dirname(__file__), "env_configs.json")
    data = get_data_from_vault(env)
    config_dict = {"urls": data['data']['contour_url'].get(env, 'No configs for this contour'),
                   "credentials": data['data']['credentials']
                   }
    with open(config_path, "w") as file:
        json.dump(config_dict, file, indent=4)


def get_env():

    if os.getenv("ENV"):
        return os.getenv("ENV")
    else:
        return ENV


def get_data_from_vault(env):

    if env == 'prod':
        vault_address = 'https://vault.wayvee.com/v1/applications/data/shopper-autotest-production'
    else:
        vault_address = 'https://vault.wayvee.com/v1/applications/data/shopper-autotest-staging'

    # vault_token = os.getenv('VAULT_TOKEN')
    vault_token = get_vault_token()

    headers = {
        "X-Vault-Token": vault_token
    }

    response = requests.get(vault_address, headers=headers)
    assert response.ok
    return response.json()['data']


def get_vault_token() -> str:
    """
    Authenticate with Vault using a Kubernetes service account token.

    Returns:
        str: The client token obtained from Vault.
    Raises:
        Exception: If authentication fails.
    """
    role = 'shopper'
    vault_address = "https://vault.wayvee.com"

    # Path to the Kubernetes service account token
    jwt_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"

    # Read the JWT token from the service account file
    with open(jwt_path, "r") as f:
        jwt = f.read()

    # Vault Kubernetes login endpoint
    url = f"{vault_address}/v1/auth/kubernetes-staging/login"

    # Payload containing the JWT and role name
    payload = {
        "jwt": jwt,
        "role": role
    }

    # Send a POST request to authenticate with Vault
    response = requests.post(url, json=payload)
    response.raise_for_status()

    # Extract the client token from the response
    token = response.json()["auth"]["client_token"]
    return token
