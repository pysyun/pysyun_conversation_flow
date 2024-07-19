import logging
import os
from logging.handlers import RotatingFileHandler

from telegram._utils.types import FilePathInput


class Logger(logging.Logger):
    def __init__(self, name: str = 'LOGGER', filepath: FilePathInput = 'logs/log.log',
                 size: int = 2, backup_count: int = 2,
                 filehandler_level=logging.WARNING, stream_handler_level=logging.DEBUG,
                 formatter: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
        super().__init__(name)

        dir_name, file_name = os.path.split(filepath)
        # Create the directory if it doesn't exist
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        sh = logging.StreamHandler()
        sh.setLevel(stream_handler_level)

        fh = RotatingFileHandler(filepath, maxBytes=size * 1024 * 1024, backupCount=backup_count)
        fh.setLevel(filehandler_level)

        log_formatter = logging.Formatter(formatter)

        fh.setFormatter(log_formatter)
        sh.setFormatter(log_formatter)

        self.addHandler(fh)
        self.addHandler(sh)


logger_instance = Logger()
