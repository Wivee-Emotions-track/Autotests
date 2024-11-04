import json
import os

from api.base_api_client import BaseApiClient

from configs.project_paths import API_RESOURCES_PATH
from helpers.dict_helper import get_data_from_json


class MeetProcessorApiClient(BaseApiClient):
    """The api client for https://meet-processor-dev.snmt.dev/docs"""

    def __init__(self,
                 endpoint,
                 token):
        self.token = token
        super().__init__(f'{endpoint}/meet-processor/', token=token)



    def get_user_processes(self):
        return self.get(url_path=f'process/user-processes/', use_token=True)



    def get_user_process(self, process_id):
        return self.get(url_path=f'process/{process_id}', use_token=True)




    def post_process_create(self, process_title:str, meet_id:str):
        """Create new interview process in extension"""
        data = json.dumps({
            "title": process_title,
            "meet_id": meet_id,
            "start_recording_timestamp": 0
        })
        return self.post(url_path=f'process/create/', data=data, use_token=True)



    def patch_process_update(self, process_id:str, title:str):
        data = get_data_from_json(os.path.join(API_RESOURCES_PATH, 'meet_processor', 'patch_process_update.json'))
        data['title']=title
        return self.patch(url_path=f'process/{process_id}/update/', data=json.dumps(data), use_token=True)



    def patch_start_processing(self, interview_marks, title, meet_id, video_url, interview_process_id):
        data = json.dumps({
            "interview_marks": interview_marks,
            "respondent_media_streams_data": None,
            "title": title,
            "meet_id": meet_id,
            "video_url": video_url,
            "interview_process_id": interview_process_id
        })
        return self.patch(url_path=f'start-processing/', data=data, use_token=True)



    def post_create_upload_link(self):
        data = json.dumps({
            "blob_name": "string",
            "content_type": "video/webm"
        })
        return self.post(url_path=f'create-upload-link/', data=data, use_token=True)