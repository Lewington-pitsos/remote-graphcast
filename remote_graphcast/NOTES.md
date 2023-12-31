## Helpful Commands

```bash
docker build . -t lewingtonpitsos/easy-graphcast:latest
docker login
docker push lewingtonpitsos/easy-graphcast:latest

docker run -e AWS_ACCESS_KEY_ID=SOME_ID -e AWS_SECRET_ACCESS_KEY=SOME_SECRET -e AWS_BUCKET=somebucket -e AWS_REGION=ap-southeast-2 -e CDS_KEY=asdfasdfa -e CDS_URL=https://asdfasdfas/sdfa/a lewingtonpitsos/easy-graphcast:latest

docker run --gpus all -it lewingtonpitsos/easy-graphcast:latest /bin/bash 
docker run --gpus all lewingtonpitsos/easy-graphcast:latest 

python app/main.py --param_file=secret_params.jso

python setup.py sdist
twine upload dist/*

python -m remote_graphcast.cli --param_file=secret_params.json
```

## Todo

- make pipy package https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
- test pipy package
- clean up dockerfile
- change date_list to forcast list
- fix logging
- make logging work when importing the actual package