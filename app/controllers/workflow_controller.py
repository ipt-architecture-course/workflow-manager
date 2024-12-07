from fastapi import APIRouter, HTTPException
from app.core.workflow_service import WorkflowService
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


router = APIRouter(prefix="/workflows", tags=["Workflows"])
workflow_service = WorkflowService()

@router.post("/start")
async def start_workflow(payload: dict):
    """
    Inicia um workflow baseado no id_profile e id_content fornecidos.
    """
    try:
        workflow_id = workflow_service.start_workflow(payload["id_profile"], payload["id_content"])
        return {"workflow_id": workflow_id, "status": "processing_started"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """
    Retorna o status de um workflow baseado no workflow_id.
    """
    status = workflow_service.get_status(workflow_id)
    if not status:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow_id": workflow_id, "status": status}
