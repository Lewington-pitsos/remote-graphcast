import logging
from pythonjsonlogger import jsonlogger

def setup_logging(level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(level)

    # Create a handler that outputs log messages as JSON
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
