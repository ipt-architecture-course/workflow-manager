from abc import ABC, abstractmethod
import logging

#configuração do o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAdapter(ABC):
    @abstractmethod
    def process(self, workflow_id, id_conteudo):
        """
        Processa o conteúdo baseado no workflow_id e id_content.
        Este método deve ser implementado por todas as subclasses.
        """
