import logging.handlers

def get_logger(name='main'):
    logger = logging.getLogger(name)

    logFormatter = logging.Formatter("%(asctime)s[%(levelname)s|%(name)s,%(lineno)s] %(message)s")
    logStreamHandler = logging.StreamHandler()
    logFileHandler = logging.handlers.RotatingFileHandler(
        filename = 'log/' + name + '.log',
        maxBytes = 10 * 1024 * 1024,
        backupCount = 10
    )

    logStreamHandler.setFormatter(logFormatter)
    logFileHandler.setFormatter(logFormatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(logStreamHandler)
    logger.addHandler(logFileHandler)

    return logger