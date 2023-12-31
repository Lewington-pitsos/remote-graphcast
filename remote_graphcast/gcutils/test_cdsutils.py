import os
from remote_graphcast.gcutils.cdsutils import *

def test_saves_correctly():
	filename = "tmp.cruft"
	save_cds_file("key", "url", filename)
	with open(filename) as f:
		content = f.read()
	
	assert content == "key: key\nurl: url\n"
	os.remove(filename)