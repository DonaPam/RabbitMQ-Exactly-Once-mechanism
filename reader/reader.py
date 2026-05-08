import pika
import time
import random
import os

reader_id = os.environ.get("READER_ID", "1")
QUEUE_NAME = "exactly_once_queue"
processed = set()

def connect_to_rabbitmq():
    print(f"[Reader {reader_id}] Connecting to RabbitMQ...")
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
            print(f"[Reader {reader_id}] Connected!")
            return connection
        except Exception as e:
            print(f"[Reader {reader_id}] Attempt {i+1}/30 failed: {e}")
            time.sleep(2)
    raise Exception("Could not connect to RabbitMQ")

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    msg_id = body.decode()
    if msg_id in processed:
        print(f"[Reader {reader_id}] DUPLICATE: {msg_id}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    processed.add(msg_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[Reader {reader_id}] PROCESSED: {msg_id}")

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)
print(f"[Reader {reader_id}] Started!")
channel.start_consuming()
