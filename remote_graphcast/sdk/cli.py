from remote_graphcast.gcutils.log_config import setup_logging
setup_logging()
from .remote_cast import cast_from_parameters
import sys

if __name__ == '__main__':
	# the first passed in argument is a filename
	cast_from_parameters(sys.argv[1])