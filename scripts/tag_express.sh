#!/bin/bash

prefix=quay.io/transparentai

for i in magenta_image_stylization-jetson_agx magenta_image_stylization-aws_c5.12xlarge magenta_image_stylization-skylake_8 magenta_image_stylization-aws_g4dn.xlarge magenta_image_stylization-aws_m6g.xlarge magenta_image_stylization-aws_c5n.xlarge
do
    echo $i
    docker tag $i ${prefix}/expressaccel-$i
    docker push ${prefix}/expressaccel-$i
done
