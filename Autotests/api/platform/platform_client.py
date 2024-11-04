import json
import os

from api.base_api_client import BaseApiClient
from configs.project_paths import API_RESOURCES_PATH
from helpers.dict_helper import get_data_from_json


class PlatformApiClient(BaseApiClient):
    """The api client for https://platform.snmt.dev/api/schema/swagger/#/"""

    def __init__(self, endpoint, user_email, user_password):
        super().__init__(f'{endpoint}/api/')
        self.user_email = user_email
        self.user_password = user_password
        self.refresh_token = None
        self.access_token_expiry = None
        self.user = None
        self.post_auth()

    #auth

    def post_auth(self):
        resp = self.post_auth_token()
        self.token = resp["access_token"]
        self.access_token_expiry = resp["access_token_expiry"]
        self.refresh_token = resp["refresh_token"]
        self.user = resp["user"]


    def post_auth_token(self):
        """Update access token by refresh token"""
        data = json.dumps({
            "email": self.user_email,
            "password": self.user_password,
            })
        return self.post(url_path='auth/token/', data=data)



    def post_token_refresh(self):
        """Update access token by refresh token"""
        data = json.dumps({
            "refresh_token": self.refresh_token
            })
        return self.post(url_path=f'auth/token/refresh/', data=data, use_token=True)

    # projects


    def get_projects(self):
        return self.get(url_path=f'projects/', use_token=True)


    def get_project(self, project_id, **kwargs):
        return self.get(url_path=f'projects/{project_id}', use_token=True, **kwargs)


    def post_projects(self, title: str):
        """Create new project"""
        data = json.dumps({
            "title": title,
            "description": "test project",
            "status": "__DRAFT__"
            })
        return self.post(url_path=f'projects/', data=data, use_token=True)


    def put_projects(self, project_id: str, title: str, interview_template: str, status: str):
        """Update all project data"""
        data = json.dumps({
            "title": title,
            "description": "test project",
            "interview_template": interview_template,
            "status": status
            })
        return self.put(url_path=f'projects/{project_id}/', data=data, use_token=True)


    def patch_projects(self, project_id: str, data):
        """Partial update project's data"""
        return self.patch(url_path=f'projects/{project_id}/', data=data, use_token=True)


    def delete_project(self, project_id):
        return self.delete(url_path=f'projects/{project_id}', use_token=True)

    # brief-form

    def get_brief(self, brief_id:str, **kwargs):
        return self.get(url_path=f'/api/brief-form/{brief_id}/', use_token=True, **kwargs)


    def get_briefs(self, project_id:str, **kwargs):
        return self.get(url_path=f'brief-form/project/{project_id}/', use_token=True, **kwargs)


    def post_brief(self, project_name:str, **kwargs):
        data = get_data_from_json(os.path.join(API_RESOURCES_PATH, 'platform', 'post_brief_form.json'))
        data['project']=project_name
        return self.post(url_path=f'brief-form/', data=json.dumps(data), use_token=True, **kwargs)


    def patch_brief(self, brief_id:str, **kwargs):
        data = get_data_from_json(os.path.join(API_RESOURCES_PATH, 'platform', 'patch_brief_form.json'))
        return self.patch(url_path=f'brief-form/{brief_id}/', data=json.dumps(data), use_token=True, **kwargs)


    def patch_save_and_send(self, brief_id:str, test_data=None, **kwargs):
        data = get_data_from_json(os.path.join(API_RESOURCES_PATH, 'platform', 'patch_brief_form_save_and_save.json'))
        if test_data:
            data = test_data
        return self.patch(url_path=f'brief-form/{brief_id}/save-and-send/', data=json.dumps(data), use_token=True, **kwargs)
