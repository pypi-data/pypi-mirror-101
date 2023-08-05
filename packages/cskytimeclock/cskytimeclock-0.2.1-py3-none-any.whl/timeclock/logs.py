from datetime import datetime
import os

CONFIG_DIR = os.path.join(os.path.expanduser("~"), '.timeclock')
LOGS_DIR = os.path.join(CONFIG_DIR, 'logs')


def message_void(message, **kwargs):
    pass


class JsonFileLogger(object):
    def __init__(self, filename_prefix='timeclock_submission_log'):
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)

        self.log_filename = os.path.join(
            LOGS_DIR, '{}_{}.json'.format(filename_prefix, datetime.now().isoformat())
        )

    def write(self, message):
        with open(self.log_filename, 'w') as log:
            log.write(message)

    def begin(self):
        self.write('[')

    def close(self):
        self.write(']')


def get_logger(filename_prefix='timeclock_submission_log'):
    return JsonFileLogger(filename_prefix)
