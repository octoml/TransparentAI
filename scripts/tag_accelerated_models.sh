#!/bin/bash

echo "tagging images"
prefix="gcr.io/octonaut-skrum"
echo $prefix

accelerated_images="magenta_image_stylization-aws_m6g.xlarge magenta_image_stylization-aws_g4dn.xlarge magenta_image_stylization-jetson_agx magenta_image_stylization-aws_c5.12xlarge magenta_image_stylization-skylake_8 magenta_image_stylization-aws_c5n.xlarge magenta_image_stylization-local"

for image in $accelerated_images
do
    echo "fullaccel-${image}"
    echo "${prefix}/fullaccel-${image}"
    echo "docker tag" "${image}" "${prefix}/fullaccel-${image}"
    docker tag "${image}" "${prefix}/fullaccel-${image}"
    docker push "${prefix}/fullaccel-${image}"
done



