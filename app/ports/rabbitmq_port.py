import pika

class RabbitMQPort:
    def __init__(self, host='localhost', queue='default'):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def publish(self, message):
        if not self.channel:
            raise Exception("Connection not established. Call connect() first.")
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)
        print(f" [x] Sent '{message}'")

    def consume(self, callback):
        if not self.channel:
            raise Exception("Connection not established. Call connect() first.")
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        if self.connection:
            self.connection.close()