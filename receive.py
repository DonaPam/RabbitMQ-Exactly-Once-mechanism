import pika

# 1. Connexion à RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Déclarer la queue (au cas où le producteur n'aurait pas été exécuté avant)
channel.queue_declare(queue='hello')

# 3. Fonction callback appelée quand un message est reçu
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

# 4. S'abonner à la queue
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()