# -*-coding:utf-8-*-
"""

logger
~~~~~~

introduction
use this model to print log into a file.

Usage
=====
>>> logger = init_logger(config_path=None)
>>> # a.py
>>> logger.info("test a.py")
>>> # b.py
>>> logger.info("test b.py")
>>> # c.py
>>> logger = get_logger("module_c")
>>> logger.info("test module_c")
>>> # d.py
>>> logger = get_logger("module_d")
>>> logger.info("test module_d")

"""
import os
import logging
import logging.config
import logging.handlers


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


def get_logger(topic):
    """get the logger object

    :param topic: data topic in config file get from command parse
    :return: logger

    """
    log_name = "./logs/%s.log" % topic
    logger = logging.getLogger("INFO")
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_name,
        when='D',
        interval=1,
        backupCount=0
    )
    formatter = logging.Formatter(
        fmt='[%(asctime)s,%(msecs)d][%(levelname)s][%(filename)s:%(lineno)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info("[INIT] init logger ...")
    logger.info("[INIT] init adapter ...")
    return logger

