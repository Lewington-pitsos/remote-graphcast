import json
import runpod

with open("credentials.json", "r") as f:
	credentials = json.load(f)

runpod.api_key = credentials['RUNPOD_KEY']

