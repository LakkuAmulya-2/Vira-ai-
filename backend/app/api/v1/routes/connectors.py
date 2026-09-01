from fastapi import APIRouter, Depends
from app.connectors.contracts import ConnectorJobRequest
from app.connectors.service import run_connector_job
from app.core.security import CurrentUser, get_current_user

router = APIRouter()

@router.post("/run")
async def run_connector(
    payload: ConnectorJobRequest,
    _: CurrentUser = Depends(get_current_user),
):
    return await run_connector_job(payload)
