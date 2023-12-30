#!/bin/bash

echo "graphcast pod start script running..."

nvcc --version

nvidia-smi

python app/cast.py
# python pad.py


