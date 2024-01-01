# Remote Graphcast

Run graphcast on a runpod GPU. Output is saved to s3. Shouldn't cost more than $0.2 for a 10 day forcast.

## Order of operations

1. Input is validated
2. A secure runpod GPU pod is spun up on your account
3. Graphcast is installed into that gpu and forcasts of your chosen length are generated for each timestamp, this takes around 10 minutes for a 10 day forcast
4. These forcasts are saved to your chosen s3 bucket, roughly 6.5GB for 10 days of forcast
5. The runpod pod is terminated
6. The program exits

## Requirements

- python 3.10+ and pip
- cds.climate credentials
- an s3 bucket
- S3 credentials to go with the bucket
- Runpod credentials

## Installation

## Example Code

```python

from remote_graphcast import remote_cast

remote_cast(
	aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
	aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY',
	aws_bucket='YOUR_AWS_BUCKET_NAME',
	cds_url='https://cds.climate.copernicus.eu/api/v2', # this is probably your CDS URL 
	cds_key='YOUR_CDS_KEY',
	forcast_list="[{'start': '2023122518', 'hours_to_forcast': 48}]", 
	# dates to forcast from, note the weird quasi-JSON format, of this string, use single quotes instead of double quotes
	# select a date in the future and it will raise an error without spinning up anything
	runpod_key='YOUR_RUNPOD_KEY',
	gpu_type_id="NVIDIA A100-SXM4-80GB", # graphcast needs at least 61GB GPU ram
	container_disk_in_gb=50, # you'll need around 40GB per 10 day forcast + a healthy 10GB buffer
)

# internally this function will keep polling the pod it spins up and the s3 bucket until it sees that all forcasts 
# are complete, then it will return


```


