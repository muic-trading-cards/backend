FROM python:3.10-slim


WORKDIR /
COPY /app /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8888", "app:create_app()"]
EXPOSE 8888