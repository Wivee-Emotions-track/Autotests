import uuid
from datetime import datetime

import allure



@allure.id("4")
@allure.title("Meet processor base flow")
@allure.label("component", "meet_extension")
@allure.label("layer", "api")
def test_meet_processor_base_flow(meet_processor_api_actions):
    with allure.step("Create Process with /meet-processor/process/create/"):
        process_title = f'AT_{str(datetime.now())}'
        test_process = meet_processor_api_actions.post_process_create(process_title=process_title,
                                                                     meet_id=str(uuid.uuid4()))
        assert test_process['status'] == '__NEW__'
    with allure.step("Create upload link with /meet-processor/create-upload-link/"):
        link = meet_processor_api_actions.post_create_upload_link()
        assert link['link_url']

    with allure.step("Update Process with /meet-processor/process/{process_id}/update/"):
        test_process = meet_processor_api_actions.patch_process_update(process_id=test_process['interview_process'],
                                                                      title=process_title)

    with allure.step("Start Processing with /meet-processor/start-processing/"):
        video_url = ('https://storage.googleapis.com/sns-interviews-dev/08-10-2024/string.mp4')
        process = meet_processor_api_actions.patch_start_processing(interview_marks=test_process['interview_marks'],
                                                                    title=test_process['title'],
                                                                    meet_id=test_process['meet_id'],
                                                                    interview_process_id=test_process[
                                                                        'interview_process_id'],
                                                                    video_url=video_url)
        assert process['status'] == '__INPROCESS__'
        assert meet_processor_api_actions.wait_for_interview_processed(process['interview_process'])
