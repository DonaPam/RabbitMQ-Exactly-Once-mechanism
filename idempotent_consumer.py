import pika
import time
import random
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='exactly_once_queue_v2', durable=True)
channel.basic_qos(prefetch_count=1)

processed = set()


def callback(ch, method, properties, body):
    msg_id = body.decode()

    if msg_id in processed:
        print(f" [!] Duplicate {msg_id} - ACK ignoring")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print(f" [↓] Received: {msg_id}")
    time.sleep(random.uniform(0.08, 0.18))  # Temps similaire à l'envoi

    # PAS de crash pour le test initial (mettez 0.0 pour commencer)
    if random.random() < 0.0:  # 0% de crash pour l'instant
        print(f" [!!!] CRASH sur {msg_id}")
        return

    processed.add(msg_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f" [✓] ACK: {msg_id}")


consumer_id = sys.argv[1] if len(sys.argv) > 1 else "?"
channel.basic_consume(queue='exactly_once_queue_v2', on_message_callback=callback, auto_ack=False)

print(f" [*] Consumer {consumer_id} ready - prefetch=1")
channel.start_consuming()