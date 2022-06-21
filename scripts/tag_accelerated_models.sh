#!/bin/bash

echo "tagging images"
prefix="quay.io/transparentai"
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



docker tag gcr.io/octonaut-skrum/fullaccel-magenta_image_stylization-aws_g4dn.xlarge:latest ${prefix}/fullaccel-magenta_image_stylization-aws_g4dn.xlarge
docker tag gcr.io/octonaut-skrum/fullaccel-magenta_image_stylization-aws_g4dn.xlarge:latest ${prefix}/style-gpu-accelerated
docker tag gcr.io/octonaut-skrum/style-cpu-accelerated:latest ${prefix}/style-cpu-accelerated
docker tag gcr.io/octonaut-skrum/style-cpu-unaccelerated:latest ${prefix}/style-cpu-unaccelerated
docker tag gcr.io/octonaut-skrum/style-gpu-unaccelerated:latest ${prefix}/style-gpu-unaccelerated


docker push ${prefix}/fullaccel-magenta_image_stylization-aws_g4dn.xlarge
docker push ${prefix}/style-gpu-accelerated
docker push ${prefix}/style-cpu-accelerated
docker push ${prefix}/style-cpu-unaccelerated
docker push ${prefix}/style-gpu-unaccelerated
