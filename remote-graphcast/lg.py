import logging
from pythonjsonlogger import jsonlogger

def setup_logging(level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(level)

    # Create a handler that outputs log messages as JSON
    handler = logging.StreamHandler()

    # Define the format for the timestamp
    log_format = '%(asctime)s %(name)s %(levelname)s %(message)s'

    formatter = jsonlogger.JsonFormatter(log_format)
    handler.setFormatter(formatter)

    logger.addHandler(handler)