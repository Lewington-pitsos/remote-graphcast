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

# to test, select a date in the future and it will raise an error

```


