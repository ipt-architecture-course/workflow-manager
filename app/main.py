from fastapi import FastAPI
from app.controllers.workflow_controller import router as workflow_router
from app.core.processor_factory import ProcessorFactory
from app.utils.config_loader import load_adapters_from_config

app = FastAPI()

processor_factory = ProcessorFactory()
load_adapters_from_config("adapters_config.json", processor_factory)

app.include_router(workflow_router)