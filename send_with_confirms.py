import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='exactly_once_queue_v2', durable=True)

channel.confirm_delivery()

message = "Message important - exactly-once test"

try:
    channel.basic_publish(
        exchange='',
        routing_key='exactly_once_queue_v2',
        body=message,
        mandatory=True
    )
    print(f" [x] Sent: {message}")
    print(" [✓] Publisher confirm received")

except pika.exceptions.UnroutableError:
    print(" [✗] Message could not be routed!")

except Exception as e:
    print(f" [✗] Error: {e}")

connection.close()