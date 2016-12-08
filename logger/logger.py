# -*-coding:utf-8-*-

import os
import logging
import logging.config


def init_logger(config_path=None):
    """get the logger object

    :param config_path: log config file
    :return: logger

    """
    path = os.path.dirname(__file__) + "/log.conf"
    config_file = config_path or path
    logging.config.fileConfig(config_file)
    logger = logging.getLogger()
    return logger
