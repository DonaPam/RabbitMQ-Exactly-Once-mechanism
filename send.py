import pika

# 1. Connexion à RabbitMQ (qui tourne dans Docker)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Créer une queue (si elle n'existe pas déjà)
channel.queue_declare(queue='hello')

# 3. Envoyer un message
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")

# 4. Fermer la connexion
connection.close()