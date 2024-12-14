import json
import logging
import pika

# Configura o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitMQAdapter:
    def __init__(self, host: str = "localhost", port: int = 5672):
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None
        self.ensure_connection()

    def ensure_connection(self):
        if not self.connection or self.connection.is_closed:
            logger.info("Establishing RabbitMQ connection...")
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port)
            )
            self.channel = self.connection.channel()

    def publish(self, queue_name: str, message: dict):
        self.ensure_connection()
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            logger.info(f"Published message to queue '{queue_name}': {message}")
        except Exception as e:
            logger.error(f"Failed to publish message to '{queue_name}': {e}")
            raise

    def consume(self, queue_name: str, callback):
        self.ensure_connection()
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)

            def wrapped_callback(ch, method, properties, body):
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
            logger.error(f"Failed to consume messages from '{queue_name}': {e}")
            raise

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                logger.info("RabbitMQ connection closed.")
            except Exception as e:
                logger.error(f"Failed to close RabbitMQ connection: {e}")

    def is_topic_available(self, queue_name: str) -> bool:
        try:
            self.channel.queue_declare(queue=queue_name, passive=True)
            return True
        except pika.exceptions.ChannelClosedByBroker:
            return False

    def get_status_from_queue(self, workflow_id: str) -> str:
        # Simulação de status baseado no workflow_id
        mock_statuses = {
            "abc123": "processing",
            "xyz789": "completed"
        }
        return mock_statuses.get(workflow_id, "not_found")
