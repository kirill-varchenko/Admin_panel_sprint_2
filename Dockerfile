FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /static
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY ./static /static