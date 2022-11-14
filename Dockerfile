FROM python:3.9 AS builder


WORKDIR /app
COPY /app /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt


# FROM nginx:alpine
# COPY --from=builder /app /app

ENV FLASK_APP=app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
EXPOSE 5000