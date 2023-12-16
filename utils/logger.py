import logging


class Logger:
    def __init__(self, name: str, log_filename: str = 'screen_rotation.log', level: int = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.log_filename = log_filename
        self.file_handler = None

    @staticmethod
    def __create_file_handler(log_file: str, level: int):
        log_format = '%(asctime)s :: [%(levelname)s] :: %(name)s :: %(message)s'
        formatter = logging.Formatter(fmt=log_format, datefmt='%Y-%m-%d %H:%M:%S')

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        return file_handler

    def __check_and_add_file_handler(self, level: int):
        if self.file_handler is None and level >= self.logger.getEffectiveLevel():
            self.file_handler = self.__create_file_handler(self.log_filename, level)
            self.logger.addHandler(self.file_handler)

    def log_debug(self, message: str):
        self.__check_and_add_file_handler(logging.DEBUG)
        self.logger.debug(message)

    def log_info(self, message: str):
        self.__check_and_add_file_handler(logging.INFO)
        self.logger.info(message)

    def log_warning(self, message: str):
        self.__check_and_add_file_handler(logging.WARNING)
        self.logger.warning(message)

    def log_error(self, message: str):
        self.__check_and_add_file_handler(logging.ERROR)
        self.logger.error(message)

    def log_critical(self, message: str):
        self.__check_and_add_file_handler(logging.CRITICAL)
        self.logger.critical(message)
