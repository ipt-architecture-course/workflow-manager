import openai
import logging
from app.ports.base_adapter import BaseAdapter

# Configura o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatGPTAdapter(BaseAdapter):
    def process(self, workflow_id: str, id_content: str):
        logger.info(f"Processing ChatGPT for workflow {workflow_id} with content ID {id_content}")
        summary = self.generate_summary(id_content)
        return {
            "status": "success",
            "workflow_id": workflow_id,
            "summary": summary
        }

    def generate_summary(self, content: str) -> str:
        """
        Chama a API do ChatGPT para gerar um resumo real.
        """
        logger.info(f"Generating summary for content ID {content}")

        try:
            # Configurar sua chave de API
            openai.api_key = "sua-chave-api-aqui"

            # Simular o prompt do ChatGPT
            response = openai.Completion.create(
                engine="text-davinci-003",  # Use o modelo desejado
                prompt=f"Generate a summary for the following content: {content}",
                max_tokens=100
            )

            # Extrair o texto gerado
            summary = response['choices'][0]['text'].strip()
            return summary
        except Exception as e:
            logger.error(f"Error while generating summary: {e}")
            return "Error: Unable to generate summary."
