FROM python:3.8.11-buster

RUN apt-get update -y && \
    apt-get install -y \
    netcat \
    unzip \
    tree


COPY ./requirements.txt /app/requirements.txt

ADD . /app

WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["bash", "dockerstart.sh"]