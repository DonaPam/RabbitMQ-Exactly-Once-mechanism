FROM python:3.10-slim

WORKDIR /app

COPY writer.py .

RUN pip install pika

CMD ["python", "-u", "writer.py"]