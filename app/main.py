from fastapi import FastAPI
from app.controllers.workflow_controller import workflow_router


app = FastAPI(title="Workflow Manager")

# Inclui os endpoints do Workflow Manager
app.include_router(workflow_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Workflow Manager"}