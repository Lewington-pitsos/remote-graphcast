import climetlab as cml
import xarray
import numpy as np
from datetime import datetime
from constants import CF_NAME_SFC

def load_predictions(pred_root):
    pred_date_data = cml.load_source("file", pred_root)
    for message in pred_date_data:
        pred_start = message.datetime()
        break

    pred = xarray.open_dataset(pred_root + '-full.nc')
    absolute_times = np.datetime64(pred_start) + pred.time.values
    pred = pred.assign_coords(time=absolute_times)
    pred = pred.reindex(lat=list(reversed(pred.lat.values)))
      
    return pred

class StateList():
	def __init__(self, start_date, forcast_length_hours, step_size, vars=CF_NAME_SFC.values()) -> None:
		self.start_date = start_date
		self.forcast_length_hours = forcast_length_hours
		self.step_size = step_size
		self.vars = vars
	
	def default_upper_bound(self):
		return self.start_date + datetime.timedelta(hours=self.forcast_length_hours)

	def dates(self, lower_bound=None, upper_bound='max'):
		wanted_dates = []
		if upper_bound == 'now':
			upper_bound = datetime.now()

		if upper_bound == 'max':
			upper_bound = self.default_upper_bound()

		for i in range(0, self.forcast_length_hours, self.step_size):
			candidate_date = self.start_date + datetime.timedelta(hours=i)
			is_wanted = True
			if lower_bound is not None:
				is_wanted = candidate_date > lower_bound
			if is_wanted and candidate_date < upper_bound:
				wanted_dates.append((i, candidate_date))
		return wanted_dates	
	
	def dates_mapped_to_hours(self, **kwargs):
		dates = self.dates(**kwargs)
		date_hours = self._map_dates_to_hours([d for _, d in dates])
		days = self._split_dates_into_days(date_hours)
		return days
	
	def dates_as_strings(self, **kwargs):
		dates = self.dates(**kwargs)
		# convert to strings
		return [d.strftime("%Y%m%d%H") for _, d in dates]

	def _map_dates_to_hours(self, dates):
		date_hours = {}
		for d in dates:
			# datetime components to string, e.g. 20231117 ensureing that leading and trailing zeros are stil there
			day = str(d.year).zfill(4) + str(d.month).zfill(2) + str(d.day).zfill(2)
			if day not in date_hours:
				date_hours[day] = []
			date_hours[day].append(d.hour)
		
		return date_hours

	def _split_dates_into_days(self, date_hours):
		days = {}
		for day, hours in date_hours.items():
			k = str(".".join([str(h) for h in hours]))
			if k not in days:
				days[k] = []
			days[k].append((day, hours))
		
		segments = []

		for k, v in days.items():
			segment_data = []
			for day, hours in v:
				segment_data.append(day)

			segments.append((segment_data, v[0][1]))
		
		return segments

