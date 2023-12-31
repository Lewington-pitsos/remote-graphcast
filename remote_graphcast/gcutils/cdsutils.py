import os
import yaml

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