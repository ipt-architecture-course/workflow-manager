import uuid
from app.core.processor_factory import processor_factory
from app.adapters.profile_adapter import ProfileAdapter

class WorkflowService:
    def __init__(self):
        self.profile_adapter = ProfileAdapter()

    def start_workflow(self, id_profile, id_conteudo):
        if not id_profile or not id_conteudo:
            raise ValueError("id_profile and id_conteudo are required.")

        profile_data = self.profile_adapter.get_profile(id_profile)
        process_type = profile_data.get("process_type")

        if not process_type:
            raise ValueError(f"No process type defined for profile {id_profile}.")

        workflow_id = str(uuid.uuid4())
        processor = processor_factory.get_processor(process_type)
        processor.process(workflow_id, id_conteudo)
        return workflow_id

    def get_workflow_status(self, workflow_id):
        return "in_progress"  # Simulado, pode ser alterado para persistência real