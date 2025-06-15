docker build -t resnet50_image .

docker run --gpus all -v /path_to_local_data:/app/data resnet50_image python3 train.py

docker run --gpus all -v /path_to_local_image:/app/images resnet50_image python3 inference.py
