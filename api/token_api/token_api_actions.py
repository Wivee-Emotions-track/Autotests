from api.token_api.token_api import TokenApi


class TokenApiActions(TokenApi):

    def get_token_id_via_name(self, token_name):

        token_list = self.get_token_list()
        for node in token_list:
            if node['name'] == token_name:
                return node['id']
