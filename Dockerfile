FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y gettext libgettextpo-dev
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY requirements-dev.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN pip install -r requirements.txt
