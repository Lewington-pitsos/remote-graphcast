import json
from datetime import datetime
import random
import climetlab as cml	

def generate_cast_id():
	adj = [
		"whispering", "forgotten", "sublime", "phantom", "mystic",
		"cosmic", "dazzling", "spectral", "fleeting", "shimmering",
		"invisible", "echoing", "intangible", "melodic", "transient",
		"prismatic", "noctilucent", "aurora", "enigmatic", "ephemeral",
		"stellar", "mythic", "azure", "crystalline", "mystifying",
		"radiant", "lucent", "polar", "celestial", "timeless",
		"cobalt", "harmonic", "infinite", "nautical", "primal",
		"solar", "wandering", "auroral", "floral", "lucent",
		"maritime", "opaline", "stellar", "twinkling", "zodiacal",
		"botanic", "coral", "dreamlike", "glacial", "harmonic",
		"ethereal", "arcane", "sylvan", "emerald", "golden",
		"silver", "moonlit", "sunlit", "twilight", "midnight",
		"dawn", "dusk", "summer", "winter", "autumn",
		"spring", "ancient", "modern", "timeless", "endless",
		"boundless", "ageless", "eternal", "everlasting", "perpetual",
		"unending", "infinite", "limitless", "unbounded", "unfathomable"
	]
	nouns = [
		"cosmos", "phantasm", "stardust", "galaxy", "oasis",
		"tempest", "artifact", "cascade", "maelstrom", "saga",
		"reverie", "illusion", "odyssey", "riddle", "miracle",
		"cosmic", "haven", "mirage", "oracle", "tapestry",
		"atlantis", "harmony", "nebulae", "pinnacle", "relic",
		"zenith", "borealis", "inferno", "oceanus", "pulsar",
		"saga", "allegory", "clarity", "expanse", "fable",
		"lagoon", "narrative", "pastoral", "rhapsody", "sonnet",
		"tundra", "cascade", "echo", "infinity", "monolith",
		"oasis", "panorama", "sphere", "torrent", "wilderness",
		"abyss", "beacon", "chronicle", "dimension", "eclipse",
		"fjord", "glacier", "horizon", "island", "jungle",
		"kaleidoscope", "labyrinth", "meadow", "nirvana", "ocean",
		"paradise", "quasar", "rainforest", "sanctuary", "tide",
		"universe", "vortex", "waterfall", "xanadu", "yonder",
		"zenith", "arcadia", "bazaar", "citadel", "dome",
		"enclave", "fortress", "grove", "hamlet", "isle"
	]

	present = datetime.now()
	time_string = present.strftime("%Y-%m-%d_%H-%M-%S")

	return f"{time_string}_{random.choice(adj)}_{random.choice(nouns)}"


def confirm_start_time_exists(start_point):
	# actually try to download era5 data for this start time if it raises an
	# exception it means that this time period is not available
	ds = cml.load_source(
		"cds",
		"reanalysis-era5-single-levels",
		param=["2t"],
		product_type="reanalysis",
		grid='60/60',
		date=start_point['start_date'],
		time=start_point['start_time'],
		lazily=True,
	) 

	ds.to_xarray() 


def parse_date_list(date_list):
	# the runpod API cannot handle double quotes so date_list is single quoted
	# we need to convert it to regular JSON
	date_list = json.loads(date_list.replace("'", '"')) 

	for start in date_list:
		start['start_time'] = int(start['start'][-2:])
		start['start_date'] = start['start'][:-2]

	return date_list
	
def get_completion_path(cast_id):
	return f"{cast_id}/.easy_graphcast_complete"

def validate_date_list(date_list, strict_start_times=True):	
	# the runpod API cannot handle double quotes so date_list is single quoted
	if '"' in date_list:
		raise ValueError('date_list cannot contain double quotes (this is a limitation of the runpod API) replace with single quotes.')

	date_list = parse_date_list(date_list)

	if strict_start_times:
		for start in date_list:
			if start['start_time'] not in [6, 18]:
				raise ValueError('you must start all graphcast forcasts at either 0600 or 1800 (see https://youtu.be/PD1v5PCJs_o?t=1915 for more information). You can disable this check by setting strict_start_times=False')

	for start in date_list:
		confirm_start_time_exists(start)
