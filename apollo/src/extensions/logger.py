import logging
import logging.config

from os import path

path_to_file = path.join(path.dirname(path.abspath(__file__)), './logger.conf')
logging.config.fileConfig(path_to_file, disable_existing_loggers=False)

logger = logging.getLogger()
