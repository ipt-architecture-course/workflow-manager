import uuid
import logging
from app.adapters.rabbitmq_adapter import RabbitMQAdapter
from app.utils.config_loader import load_config

logger = logging.getLogger(__name__)

class WorkflowService:
    def __init__(self, rabbitmq_adapter=None):
        self.config = load_config()
        self.rabbitmq = rabbitmq_adapter or RabbitMQAdapter()
        logger.debug(f"Initialized with RabbitMQAdapter={self.rabbitmq}")

    @staticmethod
    def validate_config(config: dict):
        for process_type, adapter_path in config.items():
            try:
                module_path, class_name = adapter_path.rsplit(".", 1)
                module = importlib.import_module(module_path)
                getattr(module, class_name)
            except (ImportError, AttributeError):
                raise ValueError(f"Invalid adapter configuration: {adapter_path}")

    def start_workflow(self, id_profile: str, id_content: str) -> str:
        process_type = self.get_process_type_from_profile(id_profile)
        if not process_type:
            raise ValueError(f"Invalid process type for profile: {id_profile}")

        workflow_id = str(uuid.uuid4())
        topic = f"generator.{process_type}.process"
        logger.info(f"Starting workflow: {workflow_id}, Topic: {topic}, Content ID: {id_content}")

        # Validação de publicação
        if not self.rabbitmq.is_topic_available(topic):
            raise ValueError(f"Invalid or unavailable topic: {topic}")

        try:
            self.rabbitmq.publish(topic, {
                "workflow_id": workflow_id,
                "id_content": id_content
            })
            logger.info(f"Workflow {workflow_id} published to topic {topic}")
        except Exception as e:
            logger.error(f"Failed to publish workflow {workflow_id}: {e}")
            raise

        return workflow_id

    def get_process_type_from_profile(self, id_profile: str) -> str:
        profile_mapping = {
            "1": "thumbnail",
            "2": "keywords",
            "3": "twitter",
            "4": "chatgpt",
            "5": "rabbitmq"
        }
        process_type_key = profile_mapping.get(id_profile)
        if not process_type_key:
            raise ValueError(f"Invalid profile ID: {id_profile}")
        process_type = self.config.get(process_type_key)
        print(f"DEBUG: id_profile={id_profile}, process_type={process_type}, config={self.config}")
        if not process_type:
            raise ValueError(f"Profile {id_profile} does not have a valid process type configured.")
        return process_type


    def get_status(self, workflow_id: str) -> str:
        """
        Simulação de busca de status.
        Substituir por integração com banco de dados ou cache no futuro.
        """
        try:
            status = self.rabbitmq.get_status_from_queue(workflow_id)
            if not status:
                logger.warning(f"No status found for workflow ID: {workflow_id}")
                raise ValueError(f"No status found for workflow ID: {workflow_id}")
            return status
        except Exception as e:
            logger.error(f"Failed to fetch status for workflow ID {workflow_id}: {e}")
            raise
