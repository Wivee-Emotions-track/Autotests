# -*- coding: utf-8 -*-
import os
import re

from antigate import AntiGate, AntiGateError

from log import logger


class AntiGateClient(AntiGate):

    def __init__(self):
        super().__init__(os.getenv('ANTI_CAPCHA_KEY'))

    def captcha_handler(self, screen_path):
        """
        screen_path: screen_path.jpg
        """
        capcha_id = self.send(screen_path)
        logger.debug('Antigate capcha_id:%s', capcha_id)

        try:
            answer = self.get(capcha_id)
            logger.debug("Antigate response:%s", answer)
            self.check_capcha_value_format(answer)
            return answer
        except AntiGateError as err:
            self.abuse()
            raise self.AntiCapchaException(err)

    def check_capcha_value_format(self, value):
        pattern = r'^[A-Za-z]{8,}$'
        if not value:
            self.abuse()
            raise self.AntiCapchaException('Antigate capcha value is empty')
        if not bool(re.match(pattern, value)):
            self.abuse()
            raise self.AntiCapchaException('Antigate capcha value incorrect format')

    class AntiCapchaException(Exception):
        """ Class for any API exceptions during requests."""

        def __init__(self, message=''):
            self.message = message
            logger.error(self.message)

        def __str__(self):
            return self.message
