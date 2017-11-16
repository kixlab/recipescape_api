FROM python:3.6.3-jessie
ENV PYTHONBUFFERED 1
RUN mkdir /src
ADD requirements.txt /src/
WORKDIR /src
RUN pip install -r requirements.txt
