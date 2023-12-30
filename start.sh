#!/bin/bash

echo "graphcast pod start script running..."

nvcc --version

nvidia-smi

python pad.py

