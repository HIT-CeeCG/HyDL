docker build -t vgg_image .

docker run --gpus all -v /path_to_local_data:/app/data vgg_image python3 train.py

docker run --gpus all -v /path_to_local_image:/app/images vgg_image python3 inference.py
