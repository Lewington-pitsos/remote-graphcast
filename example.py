from remote_graphcast import remote_cast

remote_cast(
	aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
	aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY',
	aws_bucket='YOUR_AWS_BUCKET_NAME',
	cds_url='https://cds.climate.copernicus.eu/api/v2', # this is probably your CDS URL 
	cds_key='YOUR_CDS_KEY',
	forcast_list="[{'start': '2023122518', 'hours_to_forcast': 48}]", # dates to forcast from, note the weird quasi-JSON format, of this string, use single quotes instead of double quotes
	runpod_key='YOUR_RUNPOD_KEY',
	gpu_type_id="NVIDIA A100 80GB PCIe", # graphcast needs at least 61GB GPU ram
	container_disk_in_gb=50, # you'll need around 40GB per 10 day forcast + a healthy 10GB buffer
)

# internally this function will keep polling the pod it spins up and the s3 bucket until it sees that all forcasts 
# are complete, then it will return