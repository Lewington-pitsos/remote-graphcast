import requests
from requests.exceptions import RequestException
import os
import yaml
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


RCFILE_PATH = "~/.cdsapirc"

def save_cds_rcfile(cds_key, cds_url):
	save_cds_file(cds_key, cds_url, RCFILE_PATH)

def save_cds_file(cds_key, cds_url, filename):

	expanded_filename = os.path.expanduser(filename)
	with open(expanded_filename, "w") as f:
		data = {
			'key': cds_key,
			'url': cds_url
		}
		yaml.dump(data, f)

def get_latest_available_date(api_url="https://cds.climate.copernicus.eu/api/v2.ui/resources/reanalysis-era5-single-levels", retries=3, timeout=5):
    for attempt in range(retries):
        try:
            result = requests.get(api_url, timeout=timeout)
            result.raise_for_status()

            data = result.json()

            date_range = data.get('structured_data', {}).get('temporalCoverage', '')
            if not date_range:
                raise ValueError("Temporal coverage not found in data")

            final_date = date_range.split('/')[1]

            return datetime.strptime(final_date, "%Y-%m-%d")

        except RequestException as e:
            logger.error(f"CDS most recent date request failed: {e}")
            if attempt == retries - 1:
                raise
        except ValueError as e:
            logger.error(f"cds most recent date data parsing error: {e}")
            raise

    raise Exception("Maximum retries reached")