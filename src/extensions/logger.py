import logging
import logging.config


logging.config.fileConfig(
    fname='./logger.conf',
    disable_existing_loggers=False
)

logger = logging.getLogger()

# logger.info('This is a info message')
# logger.debug('This is a debug message')

# try:
#     1+'a'

# except Exception:
#     logger.critical('This is a critical message', exc_info=True)

# def foo():
#     logger.warning('This is a warning message')

# foo()
