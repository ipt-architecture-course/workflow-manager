from app.ports.base_adapter import BaseAdapter
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ThumbnailAdapter(BaseAdapter):
    def process(self, workflow_id: str, id_content: str):
        """
        Implementa o processamento para gerar thumbnails.
        """
        # Simulação do processamento
        logger.info(f"Processing thumbnail for workflow {workflow_id} with content ID {id_content}")

        # Exemplo de retorno
        return {
            "status": "success",
            "workflow_id": workflow_id,
            "message": f"Thumbnail generated for content ID {id_content}"
        }
