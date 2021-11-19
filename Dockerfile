FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /static
RUN mkdir /socket
RUN chmod -R 666 /socket
WORKDIR /code
RUN apt-get -y update
RUN apt-get -y install build-essential python-dev libpython3-all-dev
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY ./static /static
