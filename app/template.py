import json
import runpod

with open("credentials.json", "r") as f:
	credentials = json.load(f)

runpod.api_key = credentials['RUNPOD_KEY']

for gpu in runpod.get_gpus():
	if gpu['memoryInGb'] > 48:
		print(gpu)

# template = runpod.create_template(
# 	name="easy-graphcast-test", 
# 	image_name="lewingtonpitsos/easy-graphcast:latest", 
# )

# print(template)
# print(template.id)