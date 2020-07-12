FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code
RUN pip3 install git+https://www.github.com/keras-team/keras-contrib.git && pip3 install -r requirements.txt

