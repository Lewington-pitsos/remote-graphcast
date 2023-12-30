## Helpful Commands

```bash
docker build . -t lewingtonpitsos/easy-graphcast:latest
docker push lewingtonpitsos/easy-graphcast:latest

docker run -e AWS_ACCESS_KEY_ID=SOME_ID -e AWS_SECRET_ACCESS_KEY=SOME_SECRET -e AWS_BUCKET=somebucket -e AWS_REGION=ap-southeast-2 -e CDS_KEY=asdfasdfa -e CDS_URL=https://asdfasdfas/sdfa/a lewingtonpitsos/easy-graphcast:latest
