FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED=1
RUN mkdir /static
RUN mkdir /socket
RUN chmod -R 666 /socket
WORKDIR /code
RUN apt-get -y update
RUN apt-get -y install build-essential
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY ./static /static
EXPOSE 8000
CMD ["uwsgi", "--ini", "configs/uwsgi/uwsgi.ini"]