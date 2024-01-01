## Links

https://data.ecmwf.int/forecasts/ this is all the ecmwf forcasts available to the public
https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form era5 archive

## Helpful Commands

```bash
docker build . -t lewingtonpitsos/easy-graphcast:latest
docker login
docker push lewingtonpitsos/easy-graphcast:latest

docker run --gpus all -e AWS_ACCESS_KEY_ID=SOME_ID -e AWS_SECRET_ACCESS_KEY=SOME_SECRET -e AWS_BUCKET=somebucket -e AWS_REGION=ap-southeast-2 -e CDS_KEY=asdfasdfa -e CDS_URL=https://asdfasdfas/sdfa/a -e GRAPHCAST_FORCAST_LIST="[{'start': '2023122518', 'hours_to_forcast': 48}]" lewingtonpitsos/easy-graphcast:latest

docker run --gpus all -it lewingtonpitsos/easy-graphcast:latest /bin/bash 
docker run --gpus all lewingtonpitsos/easy-graphcast:latest 

python app/main.py --param_file=secret_params.jso

python setup.py sdist
twine upload dist/*

python -m remote_graphcast.cli --param_file=secret_params.json
```

## Todo