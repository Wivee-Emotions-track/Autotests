import os

import pytest

from api.cabinet.cabinet_api_client import CabinetApiClient
from api.meet_processor.meet_processor_actions import MeetProcessorApiActions


@pytest.fixture(scope="function")
def cabinet_auth_token():
    """Provides token for report_builder & meet_extension api access."""
    cabinet_client = CabinetApiClient(endpoint=os.getenv('CABINET_URL'),
                                      user_id=os.getenv('CABINET_USER_ID'),
                                      password=os.getenv('CABINET_AUTH_TOKEN'))
    resp = cabinet_client.post_access_api_token_from_auth_token()
    return resp['token']

@pytest.fixture(scope="function")
def meet_processor_api_actions(cabinet_auth_token):
    return MeetProcessorApiActions(endpoint=os.getenv('MEET_PROCESSOR_URL'),
                                   token=cabinet_auth_token)
