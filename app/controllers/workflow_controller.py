from fastapi import APIRouter, HTTPException
<<<<<<< HEAD

router = APIRouter(prefix="/workflows", tags=["Workflows"])

@router.post("/start")
async def start_workflow(payload: dict):
    # Importação localizada para evitar dependências circulares
    from app.core.workflow_service import WorkflowService
    workflow_service = WorkflowService()
=======
from app.core.workflow_service import WorkflowService

router = APIRouter(prefix="/workflows", tags=["Workflows"])
workflow_service = WorkflowService()

@router.post("/start")
async def start_workflow(payload: dict):
>>>>>>> 4a1bbd2fa7007d6f5600e8226b0c8c326a83d452
    try:
        workflow_id = workflow_service.start_workflow(payload["id_profile"], payload["id_content"])
        return {"workflow_id": workflow_id, "status": "processing_started"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
<<<<<<< HEAD
    # Importação localizada para evitar dependências circulares
    from app.core.workflow_service import WorkflowService
    workflow_service = WorkflowService()
=======
>>>>>>> 4a1bbd2fa7007d6f5600e8226b0c8c326a83d452
    status = workflow_service.get_status(workflow_id)
    if not status:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow_id": workflow_id, "status": status}

<<<<<<< HEAD
=======
# Exporta o roteador
>>>>>>> 4a1bbd2fa7007d6f5600e8226b0c8c326a83d452
workflow_router = router
