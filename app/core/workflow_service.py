import uuid
from app.ports.base_adapter import BaseAdapter
from app.utils.config_loader import load_config
from app.adapters.rabbitmq_adapter import RabbitMQAdapter

class WorkflowService:
    def __init__(self):
        self.config = load_config()
        self.rabbitmq = RabbitMQAdapter()

    def start_workflow(self, id_profile: str, id_content: str) -> str:
        # Simula a comunicação com o Profile Manager
        process_type = self.get_process_type_from_profile(id_profile)
        if not process_type:
            raise ValueError("Invalid process type")

        # Obtém o adaptador do processo
        adapter_class = self.config.get(process_type)
        if not adapter_class:
            raise ValueError("Process type not supported")

        # Publica o workflow na fila do RabbitMQ
        workflow_id = str(uuid.uuid4())
        self.rabbitmq.publish(f"generator.{process_type}.process", {
            "workflow_id": workflow_id,
            "id_content": id_content
        })

        return workflow_id

    def get_status(self, workflow_id: str) -> str:
        """
        Consulta o status do workflow (mockado).
        """
        # Simulação: substituir por uma base de dados ou cache real
        return "in_progress"

    def get_process_type_from_profile(self, id_profile: str) -> str:
        """
        Simula a obtenção do tipo de processo baseado no id_profile.
        """
        # Aqui você faria uma chamada REST ao Profile Manager
        # Exemplo fixo
        return "thumbnail"
