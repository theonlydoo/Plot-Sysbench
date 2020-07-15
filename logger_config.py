#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler



def get_logger(appname):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(message)s')
    try:
        handler = TimedRotatingFileHandler('/log/%s.log' % appname,
                                            when="h",
                                            interval=1,
                                            backupCount=3)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)
        logger.debug('Starting logger for %s...' % appname)
    except:
        try:
            handler = TimedRotatingFileHandler('./%s.log' % appname,
                                            when="h",
                                            interval=1,
                                            backupCount=3)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(formatter)
            logger.addHandler(consoleHandler)
            logger.debug('Starting logger for %s...' % appname)

        except:
            import os
            print('Failed to import logger, neither ./ nor /log are writeable.')
            os._exit(1)
    return logger
