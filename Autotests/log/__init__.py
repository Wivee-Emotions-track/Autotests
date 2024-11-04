# -*- coding: utf-8 -*-
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from configs.project_paths import LOGS_PATH

LOG_FILE_MAX_SIZE = 1024 * 1024 * 1024
LOG_FILE_MAX_BACKUP_COUNT = 5

logger = logging.getLogger('common')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[pid:%(process)d]'
                              '[%(levelname)+8s]'
                              '[%(asctime)s]'
                              '[%(module)s]'
                              '[%(funcName)s:%(lineno)d] %(message)s',
                              '%d.%m.%Y %H:%M:%S')

console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logs_path = os.path.join(LOGS_PATH, 'autotest.log')

file_handler = RotatingFileHandler(filename=logs_path,
                                   maxBytes=LOG_FILE_MAX_SIZE,
                                   backupCount=LOG_FILE_MAX_BACKUP_COUNT,
                                   encoding='utf-8',
                                   mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
