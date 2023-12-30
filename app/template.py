import json
import runpod

with open("credentials.json", "r") as f:
	credentials = json.load(f)

runpod.api_key = credentials['runpod_key']

# print(runpod.get_gpus()) 

template = runpod.create_template(
	name="easy-graphcast-test", 
	image_name="lewingtonpitsos/easy-graphcast:latest", 
)

print(template)
print(template.id)