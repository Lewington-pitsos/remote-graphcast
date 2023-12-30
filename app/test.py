import os
from constants import *
from cdsutils import save_cds_rcfile
from down import download


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



save_cds_rcfile(cds_key=os.environ[CDS_KEY], cds_url=os.environ[CDS_URL])

print(os.listdir('/app'))

download()

#    test upload to s3 script works locally in docker file

# get graphcast working in the docker file locally using cpu
# get graphcast working on runpod using the GPU
