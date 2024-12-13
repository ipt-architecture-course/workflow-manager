import logging
from app.ports.base_adapter import BaseAdapter

# Configura o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeywordsAdapter(BaseAdapter):
    def process(self, workflow_id: str, id_content: str):
        """
        Implementa o processamento para gerar palavras-chave.
        """
        # Simulação do processamento
        logger.info(f"Processing keywords for workflow {workflow_id} with content ID {id_content}")

        # Exemplo de palavras-chave geradas
        keywords = ["keyword1", "keyword2", "keyword3"]

        return {
            "status": "success",
            "workflow_id": workflow_id,
            "keywords": keywords
        }
