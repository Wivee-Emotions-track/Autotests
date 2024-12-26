from api.devices.devices_api import DevicesApi


class DeviceApiActions(DevicesApi):

    def search_device_via_mac(self, mac):
        devices_list = self.get_devices()
        for device in devices_list:
            if device['macAddress'] == mac:
                print(device['id'])
                return device['id']
        return None
