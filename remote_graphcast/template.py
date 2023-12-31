import json
import runpod

with open("credentials.json", "r") as f:
	credentials = json.load(f)

runpod.api_key = credentials['RUNPOD_KEY']

# all_gpus = runpod.get_gpus()

# for gpu in all_gpus:
# 	print(gpu)

pod = runpod.create_pod(
	cloud_type="SECURE", # or else someone might snoop your session and steal your AWS/CDS credentials
	name=f"easy-graphcast1", 
	image_name="lewingtonpitsos/easy-graphcast:latest", 
	gpu_type_id="NVIDIA A100-SXM4-80GB",
	container_disk_in_gb=30
)