from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# pylint: disable=import-error
from src.config.config import Settings
from src.controller.employee.endpoint import employee_router
from src.controller.enter_record.endpoint import enter_record_router
from src.controller.machine_record.endpoint import machine_record_router
from src.controller.weekly_report.endpoint import weekly_report_router
from src.controller.analysis_server.endpoint import analysis_server_router
from src.dependencies.settings import get_settings

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router)
app.include_router(enter_record_router)
app.include_router(machine_record_router)
app.include_router(weekly_report_router)
app.include_router(analysis_server_router)

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/envSettings")
def get_env_settings(settings: Annotated[Settings, Depends(get_settings)]):
    return {"db_host": settings.db_host, "db_port": settings.db_port}
