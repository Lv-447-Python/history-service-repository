FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /history_service
WORKDIR /history_service
COPY . /history_service/
RUN make setup_docker