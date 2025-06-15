docker build -t bert_image .

docker run --gpus all -v /path_to_local_data:/app/data bert_image python3 train.py

docker run --gpus all -v /path_to_local_image:/app/images bert_image python3 inference.py
