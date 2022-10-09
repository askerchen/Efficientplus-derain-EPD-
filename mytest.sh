#!/bin/bash

for k in $(seq 3 3) 
do

version="v4_0${k}"
# cd ./models/${version}
# cnt=$'ls -l |grep "^-"|wc -l'
# echo ${cnt}

for i in $(seq 250 250 1000)
do
    echo "the version is ${version}, test epoch ${i}:"
    # echo "./models/${version}/KPN_rainy_image_epoch${i}_bs16.pth"

    python ./validation.py \
    --version ${version} \
    --no_gpu true \
    --load_name "./models/v4/${version}/KPN_rainy_image_epoch${i}_bs16.pth" \
    --save_name "./results/results_tmp" \
    --baseroot "./datasets/rain100H/test" ;
done

done