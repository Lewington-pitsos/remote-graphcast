import json
from datetime import datetime
import random

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
	time_string = present.strftime("%Y-%m-%d_%H-%M-%S")[:-3]

	return f"{time_string}_{random.choice(adj)}_{random.choice(nouns)}"



def parse_date_list(date_list):
	# the runpod API cannot handle double quotes so date_list is single quoted
	# we need to convert it to regular JSON
	date_list = json.loads(date_list.replace("'", '"')) 

	for start in date_list:
		start['start_time'] = datetime.strptime(start['start_time'], "%Y%m%d%H")

	return date_list


def validate_date_list(date_list):
	# make sure all data is available
	# make sure start times start at 0600 or 1800
	
	# the runpod API cannot handle double quotes so date_list is single quoted
	if '"' in date_list:
		raise ValueError('date_list cannot contain double quotes (this is a limitation of the runpod API) replace with single quotes.')
	
	parse_date_list(date_list)

