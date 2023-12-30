import os
import climetlab as cml	
import datetime
from statelist import StateList
import xarray
from constants import CDS_KEY, CDS_URL
import json
from cdsutils import *

# with open('credentials.json') as f:
# 	credentials = json.load(f)


# save_cds_rcfile(credentials[CDS_KEY], credentials[CDS_URL])

def download():
	p = StateList(datetime.datetime(2023, 12, 30, 6), 241, 12)
	predicted_dates = p.dates_mapped_to_hours(
		upper_bound=datetime.datetime(2023, 12, 31, 6)
	)



	print('dates to download', predicted_dates)

	all_ds = []
	for date, hours in predicted_dates:
		ds = cml.load_source(
			"cds",
			"reanalysis-era5-single-levels",
			param=["2t"],
			product_type="reanalysis",
			grid='0.25/0.25',
			date=date,
			time=hours,
			lazily=True,
		)
		all_ds.append(ds)

	print(all_ds)

	filename = 'cruft/era5/-20231220-era5.nc'
	os.makedirs(os.path.dirname(filename), exist_ok=True)

	ds = xarray.concat([d.to_xarray() for d in all_ds], dim='time')
	ds.to_netcdf(filename)

	print(ds)


if __name__ == '__main__':
	download()

# ds = ds.to_xarray()
# ds = ds.isel(time=0)

# print(dir(ds))
# print(ds.var)
# plt.imshow(ds.t2m.squeeze())
# plt.savefig('cruft/era5.png')