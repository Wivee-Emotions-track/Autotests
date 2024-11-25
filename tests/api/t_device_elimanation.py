from datetime import datetime
import requests

import allure
import pytest
from ui.pages.login_page import LoginPage
from ui.pages.analytics_page import AnalyticsPage


@pytest.fixture(scope="function")
def setup(page):
    username = "testing_admin@wayvee.com"
    password = "kz767ErQ9DvNXHuo1afB"
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username, password)


@allure.title("Delete device via id")
def test_delete_device_via_id(fixture_devices_api):
    fixture_devices_api.add_device()
    # URL-адрес вашего GraphQL сервера
    url = "https://app-staging.wayvee.com/graphql"

    # Данные для входа
    email = "dmitrijdmtirij@gmail.com"
    password = "Qwerty_0000"

    # ID устройства, которое нужно удалить
    device_id = "294"

    # 1. Аутентификация для получения токена сессии
    auth_query = """
        mutation SignIn($email: String!, $password: String!) {
            signIn(email: $email, password: $password) {
                id
                __typename
            }
        }
    """

    # Выполняем запрос на аутентификацию
    auth_response = requests.post(
        url,
        json={'query': auth_query, 'variables': {'email': email, 'password': password}}
    )

    # Проверяем, успешно ли выполнен запрос на аутентификацию
    if auth_response.status_code == 200:
        auth_cookie = auth_response.headers.get("Set-Cookie")
        if auth_cookie:
            # Извлекаем токен из строки Set-Cookie
            token = auth_cookie.split("auth-token=")[1].split(";")[0]
            print("Токен аутентификации:", token)
        else:
            print("Не удалось получить токен из Set-Cookie.")
            exit()
    else:
        print("Ошибка авторизации:", auth_response.json())
        exit()

    # 2. Запрос на удаление устройства
    delete_device_query = """
        mutation DeleteProducedDevice($id: ID!) {
            deleteProducedDevice(id: $id) {
                id
                version
                modification
                macAddress
                manufacturingDate
            }
        }
    """

    # Заголовки с токеном сессии для авторизации запроса на удаление устройства
    headers = {
        "Cookie": f"auth-token={token}"
    }

    # Выполняем запрос на удаление устройства
    delete_device_response = requests.post(
        url,
        json={'query': delete_device_query, 'variables': {'id': device_id}},
        headers=headers
    )

    # Проверяем ответ на запрос удаления устройства
    if delete_device_response.status_code == 200 and "errors" not in delete_device_response.json():
        deleted_device = delete_device_response.json()['data']['deleteProducedDevice']
        print("Устройство успешно удалено:", deleted_device)
    else:
        print("Ошибка при удалении устройства:", delete_device_response.json())


payload = {"operationName":
               "ListShops","variables":
    {"pageInput":{"page":3,"perPage":10}},
           "query":"query ListShops($userId: ID, $pageInput: PageInput) {\n  shops(pageInput: $pageInput, userId: $userId) {\n    nodes {\n      id\n      name\n      location\n      industry\n      traffic\n      openHours\n      openHoursWeekend\n      timeZone\n      createdAt\n      status\n      planUrl\n      __typename\n    }\n    page {\n      page\n      perPage\n      totalItems\n      __typename\n    }\n    __typename\n  }\n}"}

