FROM area_django:latest

WORKDIR /usr/src/api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /usr/src/api
