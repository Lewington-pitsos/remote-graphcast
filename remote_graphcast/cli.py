from .remote_cast import cast_from_parameters
import logging
logger = logging.getLogger(__name__)
import fire

if __name__ == '__main__':
	logger.setLevel(logging.INFO)
	fire.Fire(cast_from_parameters)