import pika
import time
import random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='exactly_once_queue_v2', durable=True)
channel.confirm_delivery()

message_counter = 0

print(" [*] Writer: 4-6 messages per second")
print(" [*] Press CTRL+C to stop\n")

try:
    while True:
        message_counter += 1
        message_id = f"msg-{message_counter}"

        channel.basic_publish(
            exchange='',
            routing_key='exactly_once_queue_v2',
            body=message_id,
            mandatory=True
        )
        print(f" [→] Sent: {message_id}")

        # ATTENTE plus lente : 0.15 à 0.25 secondes (4-6 msg/s)
        time.sleep(random.uniform(0.15, 0.25))

except KeyboardInterrupt:
    print(f"\n [*] Stopped. Sent: {message_counter}")
    connection.close()