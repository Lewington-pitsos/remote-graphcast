FROM ghcr.io/nvidia/jax:nightly-2023-12-28

ADD start.sh ./
ADD pad.py ./

CMD ["/start.sh"]
