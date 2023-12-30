FROM ghcr.io/nvidia/jax:nightly-2023-12-28

ADD requirements.txt ./
RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN pip install git+https://github.com/Lewington-pitsos/graphcast.git@fix-requirements
# RUN pip install tree

RUN pip install python-json-logger
RUN apt-get install libeccodes-dev -y

ADD start.sh ./
RUN chmod +x /start.sh
# ADD pad.py ./
COPY app /app

CMD ["/start.sh"]
