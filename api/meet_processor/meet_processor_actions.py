from api.meet_processor.meet_processor_api_client import MeetProcessorApiClient
from decorators.waits import repeat_until_true


class MeetProcessorApiActions(MeetProcessorApiClient):

    @repeat_until_true(steps=25, delay=5)
    def wait_for_interview_processed(self, process_id):
        return self.get_user_process(process_id)['status']=='__DONE__'