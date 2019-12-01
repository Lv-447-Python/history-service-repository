FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /history_service
WORKDIR /history_service
COPY requirements.txt /history_service/
RUN pip install -r requirements.txt
COPY . /history_service/