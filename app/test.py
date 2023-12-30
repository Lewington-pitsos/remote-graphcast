import os
from constants import *

required_variables = [
	AWS_ACCESS_KEY_ID,
	AWS_SECRET_ACCESS_KEY,
	AWS_BUCKET,
	AWS_REGION,
	CDS_URL,
	CDS_KEY,
]
print('Checking environment variables are set')
for var in required_variables:
	if var not in os.environ:
		raise Exception(f"Missing required environment variable {var}")
	else:
		print(f"{var}: {os.environ[var]}")

# create weird key file for ecmwf, 
#    test it works locally in docker file

# create upload to s3 script
#    test it works locally in docker file

# get graphcast working in the docker file locally using cpu
# get graphcast working on runpod using the GPU
