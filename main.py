import runpod
import json

with open("credentials.json", "r") as f:
	credentials = json.load(f)

runpod.api_key = credentials['runpod_key']

# Get all my pods
# pods = runpod.get_pods()

# print(pods)

# print(runpod.get_gpus()) 

# # Create a pod
pod = runpod.create_pod(
	name="test", 
	image_name="runpod/stack", 
	gpu_type_id="NVIDIA RTX A5000",
	template_id="q2xr9sm3mm",
	container_disk_in_gb=20
)

# # Stop the pod
# runpod.stop_pod(pod.id)

# # Start the pod
# runpod.start_pod(pod.id)

# # Terminate the pod
# runpod.terminate_pod(pod.id)