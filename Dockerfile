# When building a docker image for RunPod be sure to use the flag --platform linux/amd64,linux/arm64 to ensure it is compatible with the platform.
FROM tensorflow/tensorflow:latest-gpu

ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD start.sh ./
RUN chmod +x /start.sh
COPY app /app

CMD ["/start.sh"]
