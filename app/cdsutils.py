import yaml

RCFILE_PATH = "~/.cdsapirc"

def save_cds_rcfile(cds_key, cds_url):
	_save_cds_rcfile(cds_key, cds_url, RCFILE_PATH)

def _save_cds_rcfile(cds_key, cds_url, filename):
	with open(filename, "w") as f:
		data = {
			'key': cds_key,
			'url': cds_url
		}
		yaml.dump(data, f)