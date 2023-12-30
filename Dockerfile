# When building a docker image for RunPod be sure to use the flag --platform linux/amd64,linux/arm64 to ensure it is compatible with the platform.
FROM tensorflow/tensorflow:latest-gpu

ADD test.py ./

CMD ["python", "test.py"]
