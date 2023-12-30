import boto3
import time
import fire
import runpod
import json
from constants import *
import datetime
import random
from lg import setup_logging
import logging
logger = logger.getLogger(__name__)


def generate_cast_id():
    adj = [
		"whispering", "forgotten", "sublime", "phantom", "mystic",
        "cosmic", "dazzling", "spectral", "fleeting", "shimmering",
        "invisible", "echoing", "intangible", "melodic", "transient",
        "prismatic", "noctilucent", "aurora", "enigmatic", "ephemeral",
        "stellar", "mythic", "azure", "crystalline", "mystifying",
        "radiant", "lucent", "polar", "celestial", "timeless",
        "cobalt", "harmonic", "infinite", "nautical", "primal",
        "solar", "wandering", "auroral", "floral", "lucent",
        "maritime", "opaline", "stellar", "twinkling", "zodiacal",
        "botanic", "coral", "dreamlike", "glacial", "harmonic",
        "ethereal", "arcane", "sylvan", "emerald", "golden",
        "silver", "moonlit", "sunlit", "twilight", "midnight",
        "dawn", "dusk", "summer", "winter", "autumn",
        "spring", "ancient", "modern", "timeless", "endless",
        "boundless", "ageless", "eternal", "everlasting", "perpetual",
        "unending", "infinite", "limitless", "unbounded", "unfathomable"
    ]
    nouns = [
        "cosmos", "phantasm", "stardust", "galaxy", "oasis",
        "tempest", "artifact", "cascade", "maelstrom", "saga",
        "reverie", "illusion", "odyssey", "riddle", "miracle",
        "cosmic", "haven", "mirage", "oracle", "tapestry",
        "atlantis", "harmony", "nebulae", "pinnacle", "relic",
        "zenith", "borealis", "inferno", "oceanus", "pulsar",
        "saga", "allegory", "clarity", "expanse", "fable",
        "lagoon", "narrative", "pastoral", "rhapsody", "sonnet",
        "tundra", "cascade", "echo", "infinity", "monolith",
        "oasis", "panorama", "sphere", "torrent", "wilderness",
        "abyss", "beacon", "chronicle", "dimension", "eclipse",
        "fjord", "glacier", "horizon", "island", "jungle",
        "kaleidoscope", "labyrinth", "meadow", "nirvana", "ocean",
        "paradise", "quasar", "rainforest", "sanctuary", "tide",
        "universe", "vortex", "waterfall", "xanadu", "yonder",
        "zenith", "arcadia", "bazaar", "citadel", "dome",
        "enclave", "fortress", "grove", "hamlet", "isle"
    ]

    present = datetime.datetime.now()
    time_string = present.strftime("%Y-%m-%d__%H-%M-%S-%f")[:-3]

    return f"{time_string}_{random.choice(adj)}_{random.choice(nouns)}"


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
		# check if the file at bucket/id/.easy_graphcast_complete exists
		
		pod_status = runpod.get_pod(self.pod.id)

		if pod_status['status'] == 'failed':
			raise Exception(f'runpod pod {self.pod} has failed, check the logs of that pod for more details')

		is_complete = self.s3_client.head_object(Bucket=self.aws_bucket, Key=f"{self.id}/{COMPLETE_PATH}")

		return is_complete

	def upload_location(self):
		return f"s3://{self.aws_bucket}/{self.id}/"

def remote_cast(
		aws_access_key_id, 
		aws_secret_access_key, 
		aws_bucket, 
		aws_region, 
		cds_url, 
		cds_key, 
		date_list, 
		cast_id=None
	):	

	if cast_id is None:
		cast_id = generate_cast_id()

	pod = runpod.create_pod(
		name=f"easy-graphcast-{cast_id}", 
		image_name="lewingtonpitsos/easy-graphcast:latest", 
		gpu_type_id="NVIDIA RTX A5000",
		container_disk_in_gb=100,
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

	logger.info('forcast is complete', extra={'forcast_location', monitor.upload_location()})

	runpod.terminate_pod(pod.id)

	logger.info('pod terminated')


if __name__ == '__main__':
	setup_logging()
	fire.Fire(remote_cast)