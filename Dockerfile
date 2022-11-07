FROM python:3.9 AS builder


WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn


FROM nginx:alpine
COPY ./apis /app/

ENV FLASK_APP=app
CMD [flask run]
EXPOSE 5000