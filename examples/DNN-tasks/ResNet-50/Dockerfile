FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3.8 python3-pip python3-dev git wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.8 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip install --upgrade pip && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && \
    pip install numpy pandas matplotlib

ARG TASK=training

RUN if [ "$TASK" = "training" ]; then \
        pip install tensorboard && \
        echo "get ready for training environment"; \
    elif [ "$TASK" = "inference" ]; then \
        pip install flask gunicorn && \
        echo "get ready for inference environment"; \
    else \
        echo "wrong task type"; \
        exit 1; \
    fi

WORKDIR /app
COPY . /app

RUN if [ "$TASK" = "training" ]; then \
        echo "python train_resnet50.py" > /app/entrypoint.sh; \
    elif [ "$TASK" = "inference" ]; then \
        echo "python inference_server.py" > /app/entrypoint.sh; \
    fi

RUN chmod +x /app/entrypoint.sh

ENV CUDA_VISIBLE_DEVICES=0

CMD ["/bin/bash", "/app/entrypoint.sh"]
