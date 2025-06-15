docker build -t gnmt16_image .

docker run --gpus all -v /path_to_local_data:/app/data gnmt16_image python3 train.py

docker run --gpus all -v /path_to_local_image:/app/images gnmt16_image python3 inference.py
