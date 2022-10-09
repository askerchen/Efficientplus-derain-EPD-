for i in $(seq 1 1 100)
do
    echo "dealing with ${i}:";
    python ./validation.py \
    --no_gpu true \
    --load_name "./models/new_rainaug+se/KPN_rainy_image_epoch1000_bs16.pth" \
    --save_name "./results/results_tmp" \
    --baseroot "./datasets/rain100H/test" ;
done