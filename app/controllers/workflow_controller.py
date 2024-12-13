from fastapi import APIRouter, HTTPException
from app.core.workflow_service import WorkflowService

router = APIRouter(prefix="/workflows", tags=["Workflows"])
workflow_service = WorkflowService()

@router.post("/start")
async def start_workflow(payload: dict):
    try:
        workflow_id = workflow_service.start_workflow(payload["id_profile"], payload["id_content"])
        return {"workflow_id": workflow_id, "status": "processing_started"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    status = workflow_service.get_status(workflow_id)
    if not status:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow_id": workflow_id, "status": status}

# Exporta o roteador
workflow_router = router
