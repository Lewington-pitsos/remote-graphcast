FROM runpod/pytorch:2.1.1-py3.10-cuda12.1.1-devel-ubuntu22.04

RUN pip uninstall -y torch

ADD requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install -U "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

COPY remote_graphcast ./remote_graphcast
ADD start.sh ./
RUN chmod +x ./start.sh

CMD ["./start.sh"]
