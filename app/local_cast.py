import json
from cast import cast_all
from constants import *

with open("credentials.json", "r") as f:
	credentials = json.load(f)

cast_all(
	aws_access_key_id=credentials[AWS_ACCESS_KEY_ID], 
	aws_secret_access_key=credentials[AWS_SECRET_ACCESS_KEY], 
	bucket_name=credentials[AWS_BUCKET],
	cds_url=credentials[CDS_URL],
	cds_key=credentials[CDS_KEY],
	date_list='[{"start_time": "2023122518", "hours_to_forcast": 48}]',
	cast_id='test_id'
)