from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.workflows.repository import WorkflowRepository

router = APIRouter()


@router.get("/{workflow_id}")
async def get_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    run = await WorkflowRepository(db).get(workflow_id)
    if run is None or run.user_id != user.id:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {
        "id": run.id,
        "status": run.status,
        "current_step": run.current_step,
        "state": run.state,
        "error": run.error,
    }
