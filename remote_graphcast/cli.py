from .log_config import setup_logging
setup_logging()
from .remote_cast import cast_from_parameters
import fire

if __name__ == '__main__':
	fire.Fire(cast_from_parameters)