from fastapi import APIRouter, HTTPException
from app.core.workflow_service import WorkflowService

router = APIRouter()
workflow_service = WorkflowService()

@router.post("/workflows/start")
async def start_workflow(payload: dict):
    try:
        workflow_id = workflow_service.start_workflow(payload["id_profile"], payload["id_conteudo"])
        return {"status_code": 200, "workflow_id": workflow_id, "status": "processing_started"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/workflows/status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    try:
        status = workflow_service.get_workflow_status(workflow_id)
        return {"status_code": 200, "workflow_id": workflow_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")