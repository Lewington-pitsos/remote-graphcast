import os
from cdsutils import *

def test_saves_correctly():
	filename = "tmp.cruft"
	_save_cds_rcfile("key", "url", filename)
	with open(filename) as f:
		content = f.read()
	
	assert content == "key: key\nurl: url\n"
	os.remove(filename)