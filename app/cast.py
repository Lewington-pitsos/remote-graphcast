import os
import json
import boto3
from cdsutils import save_cds_rcfile
import logging
logging.basicConfig(level=logging.INFO)
from ai_models_graphcast.model import GraphcastModel
from datetime import datetime
from botocore.exceptions import NoCredentialsError
from constants import *


def validate_date_list(date_list):
	pass

def parse_date_list(date_list):
	date_list = json.loads(date_list)

	for start in date_list:
		start['start'] = datetime.strptime(start['start'], "%Y%m%d%H")

	return date_list

def cast_all(
		aws_access_key_id, 
		aws_secret_access_key, 
		bucket_name,
		cds_url,
		cds_key,
		date_list,		
	):

	save_cds_rcfile(cds_key=cds_key, cds_url=cds_url)
	date_list = parse_date_list(date_list)
	s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	

	dir_path = 'cruft/'
	for start_point in date_list:
		date = start_point['start'].strftime("%Y%m%d")
		time = int(start_point['start'].strftime("%H"))
		dt = datetime.now().strftime("%Y%m%d%H")
		hours_to_forcast = start_point['hours_to_forcast']

		gc = GraphcastModel(
			input="cds", 
			output="file", 
			download_assets=True, 
			path=f'{dir_path}{dt}-output', 
			metadata={}, 
			model_args={}, 
			assets_sub_directory=dir_path,
			assets=dir_path,
			date=date, # just the date part 
			time=time, # just the time part
			staging_dates = None, # alternatively, a list of dates, as opposed to the single date/time
			debug=True,
			lead_time=hours_to_forcast, # the number of hours to forcast 
			only_gpu=True,
			archive_requests=f"{dir_path}archive",
			hindcast_reference_year=None,
		)

		gc.run()

	for subdir, _, files in os.walk(dir_path):
		for file in files:
			full_path = os.path.join(subdir, file)
			with open(full_path, 'rb') as data:
				try:
					s3_client.upload_fileobj(data, bucket_name, full_path[len(dir_path)+1:])
					print(f"File {file} uploaded successfully")
				except NoCredentialsError:
					print("Credentials not available")



required_variables = [
	AWS_ACCESS_KEY_ID,
	AWS_SECRET_ACCESS_KEY,
	AWS_BUCKET,
	AWS_REGION,
	CDS_URL,
	CDS_KEY,
	GRAPHCAST_DATE_LIST
]

print('Checking environment variables are set')
for var in required_variables:
	if var not in os.environ:
		raise Exception(f"Missing required environment variable {var}")
	else:
		print(f"{var}: {os.environ[var]}")



print('home', os.listdir('~/'))
save_cds_rcfile(cds_key=os.environ[CDS_KEY], cds_url=os.environ[CDS_URL])

print(os.listdir('/app'))
print('home', os.listdir('~/'))
