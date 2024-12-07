import json
import logging
import pika

# Configura o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitMQAdapter:
    def __init__(self, host: str = "localhost", port: int = 5672):
        """
        Inicializa a conexão com o RabbitMQ.
        """
        self.host = host
        self.port = port
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port)
            )
            self.channel = self.connection.channel()
            logger.info(f"Connected to RabbitMQ on {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def publish(self, queue_name: str, message: dict):
        """
        Publica uma mensagem na fila especificada.

        :param queue_name: Nome da fila no RabbitMQ
        :param message: Mensagem a ser enviada (dicionário JSON)
        """
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2  # Garante que a mensagem será persistida
                )
            )
            logger.info(f"Published message to queue '{queue_name}': {message}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    def consume(self, queue_name: str, callback):
        """
        Consome mensagens de uma fila especificada.

        :param queue_name: Nome da fila no RabbitMQ
        :param callback: Função a ser chamada quando uma mensagem for consumida
        """
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)

            def wrapped_callback(ch, method, properties, body):
                """
                Envolve o callback do consumidor para tratar mensagens como JSON.
                """
                try:
                    message = json.loads(body)
                    logger.info(f"Consumed message from queue '{queue_name}': {message}")
                    callback(message)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

            self.channel.basic_consume(queue=queue_name, on_message_callback=wrapped_callback)
            logger.info(f"Consuming messages from queue '{queue_name}'")
            self.channel.start_consuming()
        except Exception as e:
            logger.error(f"Failed to consume messages: {e}")
            raise

    def close_connection(self):
        """
        Fecha a conexão com o RabbitMQ.
        """
        try:
            self.connection.close()
            logger.info("RabbitMQ connection closed.")
        except Exception as e:
            logger.error(f"Failed to close RabbitMQ connection: {e}")
