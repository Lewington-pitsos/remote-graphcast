import boto3
import time
import fire
import runpod
import json
from constants import *
from inpututils import *
from lg import setup_logging
import logging
logger = logging.getLogger(__name__)


with open("credentials.json", "r") as f:
	credentials = json.load(f)

runpod.api_key = credentials['runpod_key']

class UploadMonitor():
	def __init__(self, pod, aws_access_key_id, aws_secret_access_key, aws_bucket, aws_region, cast_id) -> None:
		self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
		self.pod = pod
		self.id = cast_id
		self.aws_bucket = aws_bucket
		self.aws_region = aws_region

	def is_complete(self):
		pod = runpod.get_pod(self.pod['id'])

		if not pod:
			raise Exception(f'runpod pod {self.pod} was terminated prematurely, output of runpod.get_pod is: {pod}')

		is_complete = self.s3_client.head_object(Bucket=self.aws_bucket, Key=f"{self.id}/{COMPLETE_PATH}")

		return is_complete

	def upload_location(self):
		return f"s3://{self.aws_bucket}/{self.id}/"

def _remote_cast(parameters_file=None, **kwargs):
	if parameters_file is not None:
		with open(parameters_file, "r") as f:
			parameters = json.load(f)
		kwargs = parameters

	remote_cast(**kwargs)

def remote_cast(
		aws_access_key_id, 
		aws_secret_access_key, 
		aws_bucket, 
		aws_region, 
		cds_url, 
		cds_key, 
		date_list, 
		cast_id=None,
		gpu_type_id="NVIDIA RTX A4000",
		container_disk_in_gb=100
	):	

	validate_date_list(date_list)

	if cast_id is None:
		cast_id = generate_cast_id()

	pod = runpod.create_pod(
		name=f"easy-graphcast-{cast_id}", 
		image_name="lewingtonpitsos/easy-graphcast:latest", 
		gpu_type_id=gpu_type_id,
		container_disk_in_gb=container_disk_in_gb,
		env={
			AWS_ACCESS_KEY_ID: aws_access_key_id,
			AWS_SECRET_ACCESS_KEY: aws_secret_access_key,
			AWS_BUCKET: aws_bucket,
			AWS_REGION: aws_region,
			CDS_KEY: cds_key,
			CDS_URL: cds_url,
			DATE_LIST: date_list,
			CAST_ID: cast_id			
		}
	)
	
	logger.debug("forcasting pod created", extra={'pod_info': pod})
	monitor = UploadMonitor(pod, aws_access_key_id, aws_secret_access_key, aws_bucket, cast_id)

	while not monitor.is_complete():
		time.sleep(60)
		logger.info('polling for upload completion, all systems green')

	logger.info('easy-graphcast forcast is complete', extra={'forcast_location', monitor.upload_location()})

	runpod.terminate_pod(pod.id)

	logger.info('pod terminated')


if __name__ == '__main__':
	setup_logging()
	fire.Fire(_remote_cast)