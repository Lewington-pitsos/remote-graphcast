import os
import json
import boto3
import fire
from cdsutils import save_cds_rcfile
import logging
logging.basicConfig(level=logging.INFO)
from ai_models_graphcast.model import GraphcastModel
from datetime import datetime
from botocore.exceptions import NoCredentialsError

sl = StateList(datetime(2023, 12, 20, 6), 240, step_size=240)


# filename = 'cruft/era5/-16-era5.nc'
# os.makedirs(os.path.dirname(filename), exist_ok=True)


def validate_date_list(date_list):
	pass

def parse_date_list(date_list):
	date_list = json.loads(date_list)

	for start in date_list:
		start['start'] = datetime.strptime(start['start'], "%Y%m%d%H")

	return date_list

def main(
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

		

	

if __name__ == '__main__':
	fire.Fire(main)