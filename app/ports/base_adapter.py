from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    @abstractmethod
    def process(self, workflow_id, id_conteudo):
        pass