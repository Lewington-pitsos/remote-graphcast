import runpod
import json

with open("credentials.json", "r") as f:
	credentials = json.load(f)

runpod.api_key = credentials['runpod_key']

# print(runpod.get_gpus()) 

pod = runpod.create_pod(
	name="test", 
	image_name="lewingtonpitsos/easy-graphcast:latest", 
	gpu_type_id="NVIDIA RTX A5000",
	template_id="1lid92ziww",
	container_disk_in_gb=100,
	env={
		"AWS_ACCESS_KEY_ID": credentials['aws_access_key_id'],
		"AWS_SECRET_ACCESS_KEY": credentials['aws_secret_access_key'],
		'AWS_BUCKET': credentials['aws_bucket'],
	}
)


print(pod)