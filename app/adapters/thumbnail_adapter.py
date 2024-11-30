from app.ports.base_adapter import BaseAdapter

class ThumbnailAdapter(BaseAdapter):
    def process(self, workflow_id, id_conteudo):
        print(f"Processing thumbnail for workflow {workflow_id} with content {id_conteudo}")