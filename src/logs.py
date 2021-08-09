import logging
import settings


class Logs:
    def __init__(self):
        self.log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def error(self, msg):
        error_logger = logging.getLogger(__name__)
        e_handler = logging.FileHandler(settings.log_file('error.log'))
        e_handler.setLevel(logging.ERROR)
        e_handler.setFormatter(self.log_format)
        error_logger.addHandler(e_handler)
        error_logger.error(msg, exc_info=True)

    def warning(self, msg):
        warning_logger = logging.getLogger(__name__)
        w_handler = logging.FileHandler(settings.log_file('warning.log'))
        w_handler.setLevel(logging.WARNING)
        w_handler.setFormatter(self.log_format)
        warning_logger.addHandler(w_handler)
        warning_logger.warning(msg)

    @staticmethod
    def info(msg):
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.info(msg)
