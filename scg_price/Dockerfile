FROM python:3.8
RUN apt-get update
RUN mkdir app
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN python -m pip install wheel
COPY scraper_requirements.txt /app
RUN python -m pip install -r scraper_requirements.txt
ADD . / /app/
