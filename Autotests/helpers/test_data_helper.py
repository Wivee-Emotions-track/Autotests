import json
import os

from configs.project_paths import TEST_DATA_PATH
from helpers.dict_helper import get_data_from_json
from log import logger

def load_test_data(test_info):
    """
        Fixture returns test_data.json path
    """
    test_method_name = test_info.originalname
    test_folder = test_info.fspath.dirname
    test_data_folder = test_folder.split('tests', 1)[1].replace('\\tests\\', '')
    test_data_path = os.path.join(TEST_DATA_PATH, test_data_folder, f'{test_method_name}.json')
    try:
        get_data_from_json(test_data_path)
        return get_data_from_json(test_data_path)
    except FileNotFoundError:
        logger.debug(f'No test_data file in {test_data_path}')
    except json.JSONDecodeError:
        raise ValueError(f"Error reading JSON from file: {test_data_path}")
