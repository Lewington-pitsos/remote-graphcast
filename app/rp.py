from constants import *
import json
import runpod
from lg import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

with open("credentials.json", "r") as f:
	credentials = json.load(f)

runpod.api_key = credentials[RUNPOD_KEY]


pod = runpod.create_pod(
	name="test", 
	image_name="lewingtonpitsos/easy-graphcast:latest", 
	gpu_type_id="NVIDIA RTX A4000",
	container_disk_in_gb=100,
	env={
		AWS_ACCESS_KEY_ID: credentials[AWS_ACCESS_KEY_ID],
		AWS_SECRET_ACCESS_KEY: credentials[AWS_SECRET_ACCESS_KEY],
		AWS_BUCKET: credentials[AWS_BUCKET],
		CDS_KEY: credentials[CDS_KEY],
		CDS_URL: credentials[CDS_URL],
		DATE_LIST: "[{'start_time': '2023122518', 'hours_to_forcast': 48}]",
		CAST_ID: 'test_cast'
	}
)

logger.info('pod', extra={'type':type(pod), 'pod': pod, 'dir': dir(pod)})

pod2 = runpod.get_pod(pod['id'])

logger.info('pod2', extra={'pod': pod2})

runpod.terminate_pod(pod['id'])

pod3 = runpod.get_pod(pod['id'])

logger.info('pod3', extra={'pod': pod3})

