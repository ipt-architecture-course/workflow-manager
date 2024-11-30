from app.ports.base_adapter import BaseAdapter

class KeywordsAdapter(BaseAdapter):
    def process(self, workflow_id, id_conteudo):
        print(f"Processing keywords for workflow {workflow_id} with content {id_conteudo}")