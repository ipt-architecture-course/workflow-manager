import logging
import tweepy
from app.ports.base_adapter import BaseAdapter

# Configura o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterAdapter(BaseAdapter):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Inicializa o adaptador com credenciais do Twitter.
        """
        self.auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        self.api = tweepy.API(self.auth)

    def process(self, workflow_id: str, id_content: str):
        """
        Implementa o processamento para postar um tweet relacionado ao workflow.
        """
        logger.info(f"Processing Twitter post for workflow {workflow_id} with content ID {id_content}")

        # Simulação de mensagem baseada no conteúdo
        message = self.generate_message(id_content)

        # Posta o tweet
        tweet = self.post_tweet(message)

        return {
            "status": "success",
            "workflow_id": workflow_id,
            "tweet_id": tweet.id,
            "message": tweet.text,
        }

    def generate_message(self, id_content: str) -> str:
        """
        Gera uma mensagem de exemplo para postagem no Twitter.
        """
        logger.info(f"Generating message for content ID {id_content}")
        return f"New content available! Check it out: Content ID {id_content} #WorkflowManager"

    def post_tweet(self, message: str):
        """
        Posta um tweet com a mensagem fornecida.
        """
        try:
            tweet = self.api.update_status(status=message)
            logger.info(f"Tweet posted successfully: {tweet.text}")
            return tweet
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            raise
