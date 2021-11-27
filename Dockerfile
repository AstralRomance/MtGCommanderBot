FROM python:3.8
RUN apt-get update
RUN mkdir app
WORKDIR /app

# create environment variable
COPY bot_requirements.txt /app
RUN python -m pip install --upgrade pip
RUN python -m pip install wheel
RUN python -m pip install -r bot_requirements.txt
