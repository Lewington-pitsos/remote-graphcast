import boto3
import time
import runpod
import json
from remote_graphcast.gcutils.constants import *
from remote_graphcast.gcutils.inpututils import *
import logging
logger = logging.getLogger(__name__)

class UploadMonitor():
	def __init__(self, pod, aws_access_key_id, aws_secret_access_key, aws_bucket, cast_id) -> None:
		self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
		self.pod = pod
		self.cast_id = cast_id
		self.aws_bucket = aws_bucket

	def is_complete(self):
		pod = runpod.get_pod(self.pod['id'])

		if not pod:
			raise Exception(f'runpod pod {self.pod} was terminated prematurely, output of runpod.get_pod is: {pod}')

		try:		
			self.s3_client.head_object(Bucket=self.aws_bucket, Key=get_completion_path(self.cast_id))
			return True
		except Exception as e:
			if hasattr(e, 'response') and e.response['Error'].get('Code') == "404":
				logger.debug(f'upload not complete, expected_s3_error {e}')
				return False
			else: 
				raise e

	def upload_location(self):
		return f"s3://{self.aws_bucket}/{self.cast_id}/"

def cast_from_parameters(param_file=None, **kwargs):
	if param_file is not None:
		assert param_file.endswith(".json"), "param_file must be a json file"

		with open(param_file, "r") as f:
			parameters = json.load(f)
		kwargs = parameters

	remote_cast(**kwargs)

def validate_gpu_type_id(gpu_type_id):
	if gpu_type_id == "NVIDIA A100 80GB PCIe":
		logger.warn(f'{gpu_type_id} is known to crash on runpod around 50% of the time when used in combination with the remote graphcast docker image. We suggest using NVIDIA A100-SXM4-80GB instead')

def validate(gpu_type_id, forcast_list, strict_start_times):
	validate_gpu_type_id(gpu_type_id)
	validate_forcast_list(forcast_list, strict_start_times)

def remote_cast(
		aws_access_key_id, 
		aws_secret_access_key, 
		aws_bucket, 
		cds_url, 
		cds_key, 
		forcast_list, 
		runpod_key,
		cast_id=None,
		gpu_type_id="NVIDIA A100-SXM4-80GB", # graphcast needs at least 61GB GPU ram
		container_disk_in_gb=50,
		strict_start_times=True
	):	

	if cast_id is None:
		cast_id = generate_cast_id()
		logger.info(f'cast_id generated {cast_id}')
	
	logger.info(f'validating input')
	validate(gpu_type_id, forcast_list, strict_start_times)
	runpod.api_key = runpod_key
	
	pod = runpod.create_pod(
		cloud_type="SECURE", # or else someone might snoop your session and steal your AWS/CDS credentials
		name=f"easy-graphcast-{cast_id}", 
		image_name="lewingtonpitsos/easy-graphcast:latest", 
		gpu_type_id=gpu_type_id,
		container_disk_in_gb=container_disk_in_gb,
		env={
			AWS_ACCESS_KEY_ID: aws_access_key_id,
			AWS_SECRET_ACCESS_KEY: aws_secret_access_key,
			AWS_BUCKET: aws_bucket,
			CDS_KEY: cds_key,
			CDS_URL: cds_url,
			FORCAST_LIST: forcast_list,
			CAST_ID: cast_id			
		}
	)
	
	logger.info(f"forcasting pod created, id: {pod['id']}, machineId: {pod['machineId']}, machine: {pod['machine']}")
	monitor = UploadMonitor(pod, aws_access_key_id, aws_secret_access_key, aws_bucket, cast_id)

	while not monitor.is_complete():
		logger.info('checking runpod and s3 for forcast status: all systems green')
		time.sleep(60)

	logger.info(f'easy-graphcast forcast is complete saved to, {monitor.upload_location()}')

	runpod.terminate_pod(pod['id'])

	logger.info('pod terminated')

	return monitor.upload_location()


