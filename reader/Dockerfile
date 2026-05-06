FROM python:3.10-slim

WORKDIR /app

COPY reader.py .

RUN pip install pika

CMD ["python", "-u", "reader.py"]