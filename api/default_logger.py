import os, logging
from api import config_params
from datetime import datetime
from logging.handlers import RotatingFileHandler



log_folder = os.path.realpath("../logs")

def configure_log_folder(file_name):
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    logs_path_root = log_folder + "/csv_parser/"
    logs_path = logs_path_root + file_name

    if not os.path.exists(logs_path_root):
        os.mkdir(logs_path_root)

    if os.path.exists(logs_path):
        os.remove(logs_path)

    return logs_path


def conf_logger(log_level):
    filename = 'csv-parser-{:%Y-%m-%d %H-%M-%S}.log'.format(datetime.now())
    logs_path = configure_log_folder(filename)

    logger = logging.getLogger("csv_parser")
    logger.setLevel(logging.DEBUG)
    fileHandler = RotatingFileHandler(
        logs_path, maxBytes=5000000, backupCount=5
    )

    fileHandler.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s - %(levelname)s - module:%(filename)s#%(lineno)d '
        '- func: "%(funcName)s"] message: "%(message)s"'
    )

    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger

logger = conf_logger(config_params.LOG_LEVEL.upper())

