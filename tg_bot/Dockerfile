FROM python:3.8
RUN apt-get update
RUN mkdir app
WORKDIR /app

ENV SCRAPY_CONTAINER="localhost"
ENV SCRAPY_PORT=9080
ENV TG_API_KEY=<API KEY MUST BE HERE>
COPY bot_requirements.txt /app
RUN python -m pip install --upgrade pip
RUN python -m pip install wheel
RUN python -m pip install -r bot_requirements.txt
ADD . / /app/
