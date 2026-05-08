import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='exactly_once_queue_v2', durable=True)

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    print(f" [x] Processing...")
    time.sleep(1)
    print(f" [x] Sending ACK")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='exactly_once_queue_v2', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. Press CTRL+C to exit')
channel.start_consuming()