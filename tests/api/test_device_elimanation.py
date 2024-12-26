import allure
import pytest


@pytest.fixture()
def fixture_add_device_add_delete(fixture_industrial_api, fixture_devices_api):
    device_mac = fixture_industrial_api.add_device(mac="d8:3a:dd:c3:52:b3")
    yield device_mac


@allure.title("Delete device via id")
def test_delete_device_via_id(fixture_devices_api, fixture_add_device_add_delete):
    device_mac = fixture_add_device_add_delete
    device_id = fixture_devices_api.search_device_via_mac(device_mac)
    fixture_devices_api.delete_device(device_id)
    assert not fixture_devices_api.search_device_via_mac(device_mac), 'Device was not deleted'
