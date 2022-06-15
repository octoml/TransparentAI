#!/bin/bash

source ../venv/bin/activate

for i in a b c d e f g h i j k:
do
    MODEL_ENDPOINT=localhost:8800 MODEL_NAME=magenta_arbitrary_image_stylization_v1_256_2_tar_gz python test.py &
    sleep 1
done

