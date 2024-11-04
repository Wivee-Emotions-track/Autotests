from api.platform.platform_client import PlatformApiClient


class PlatformApiActions(PlatformApiClient):

    def update_access_token(self):
        new_token_info = self.post_token_refresh()
        self.token = new_token_info["access_token"]
        self.access_token_expiry = new_token_info["access_token_expiry"]
        self.refresh_token = new_token_info["refresh_token"]
