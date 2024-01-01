from remote_graphcast.gcutils.log_config import setup_logging
setup_logging()

import os
import boto3
from ai_models_graphcast.model import GraphcastModel
from botocore.exceptions import NoCredentialsError
from remote_graphcast.gcutils.cdsutils import save_cds_rcfile
from remote_graphcast.gcutils.inpututils import parse_forcast_list, get_completion_path
from remote_graphcast.gcutils.constants import *
import shutil
import logging

logger = logging.getLogger(__name__)

def upload_completion_file(client, aws_bucket, cast_id):
	local_complete_file = '/tmp/.easy_graphcast_complete'

	with open(local_complete_file, 'w') as f:
		f.write('complete')
	
	client.upload_file(local_complete_file, aws_bucket, get_completion_path(cast_id))	

def cast_all(
		aws_access_key_id, 
		aws_secret_access_key, 
		aws_bucket,
		cds_url,
		cds_key,
		forcast_list,	
		cast_id
	):

	save_cds_rcfile(cds_key=cds_key, cds_url=cds_url)
	logger.debug('cds credentials file created')
	forcast_list = parse_forcast_list(forcast_list)
	s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	logger.debug('s3 client set up')

	tmp_dir = '/tmp/'
	dir_path = f'{tmp_dir}{cast_id}/'
	os.makedirs(dir_path, exist_ok=True)

	for start_point in forcast_list:
		date = start_point['start_date']
		time = start_point['start_time']
		dt = start_point['start']
		hours_to_forcast = start_point['hours_to_forcast']

		gc = GraphcastModel(
			input="cds", 
			output="file", 
			download_assets=True, 
			path=f'{dir_path}{dt}-output', 
			metadata={}, 
			model_args={}, 
			assets_sub_directory=tmp_dir,
			assets=tmp_dir,
			date=date, # just the date part 
			time=time, # just the time part
			staging_dates = None, # alternatively, a list of dates, as opposed to the single date/time
			debug=True,
			lead_time=hours_to_forcast, # the number of hours to forcast 
			only_gpu=True,
			archive_requests=None,
			hindcast_reference_year=None,
		)

		gc.run()

		os.makedirs(exist_ok=True, name=dir_path)

		with open(f'{dir_path}{dt}-output', 'w') as f:
			f.write(f"forcast complete for {start_point['start_time']}")

		logger.info(f"forcast complete for {start_point['start_time']}")


		for subdir, _, files in os.walk(dir_path):
			for file in files:
				full_path = os.path.join(subdir, file)
				s3_path = "/".join(full_path.split('/')[2:])

				with open(full_path, 'rb') as data:
					s3_client.upload_fileobj(data, aws_bucket, s3_path)
					logger.debug(f"File {s3_path} uploaded successfully from {full_path}")
	
		shutil.rmtree(dir_path)

	logger.info(f"all forcasts complete for {cast_id}, uploading to s3")
	upload_completion_file(s3_client, aws_bucket, cast_id)

	logger.info(f"upload complete for {cast_id}")

if __name__ == "__main__":
	required_variables = [
		AWS_ACCESS_KEY_ID,
		AWS_SECRET_ACCESS_KEY,
		AWS_BUCKET,
		CDS_URL,
		CDS_KEY,
		FORCAST_LIST,
		CAST_ID
	]

	logger.debug('Checking environment variables are set')
	for var in required_variables:
		if var not in os.environ:
			raise Exception(f"Missing required environment variable {var}")
		else:
			logger.debug(f"{var}: {os.environ[var]}")

	cast_all(
		aws_access_key_id=os.environ[AWS_ACCESS_KEY_ID], 
		aws_secret_access_key=os.environ[AWS_SECRET_ACCESS_KEY], 
		aws_bucket=os.environ[AWS_BUCKET],
		cds_url=os.environ[CDS_URL],
		cds_key=os.environ[CDS_KEY],
		forcast_list=os.environ[FORCAST_LIST],
		cast_id=os.environ[CAST_ID],
	)