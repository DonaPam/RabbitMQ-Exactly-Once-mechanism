import pika
import time
import random
import os
import socket

writer_id = os.environ.get("WRITER_ID", "1")
QUEUE_NAME = "exactly_once_queue"

def connect_to_rabbitmq():
    print(f"[Writer {writer_id}] Connecting to RabbitMQ...")
    for i in range(30):
        try:
            credentials = pika.PlainCredentials('user', 'password')
            parameters = pika.ConnectionParameters(
                host='rabbitmq',
                port=5672,
                credentials=credentials,
                connection_attempts=1
            )
            connection = pika.BlockingConnection(parameters)
            print(f"[Writer {writer_id}] Connected!")
            return connection
        except Exception as e:
            print(f"[Writer {writer_id}] Attempt {i+1}/30 failed: {e}")
            time.sleep(2)
    raise Exception("Could not connect to RabbitMQ")

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)
channel.confirm_delivery()

counter = 0
print(f"[Writer {writer_id}] Started!")

while True:
    counter += 1
    msg = f"msg-{int(time.time()*1000)}-{writer_id}-{counter}"
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=msg, mandatory=True)
    print(f"[Writer {writer_id}] Sent: {msg}")
    time.sleep(random.uniform(0.1, 0.2))
