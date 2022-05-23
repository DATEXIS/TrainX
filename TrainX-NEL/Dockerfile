FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime

RUN apt update && apt install -y git libopenblas-base libomp-dev

RUN mkdir -p /biencoder
WORKDIR /biencoder

COPY src/biencodernel ./src/biencodernel/
COPY src/*.py ./src/
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT python src/run.py