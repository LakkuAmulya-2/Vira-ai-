from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.workflows.persistence import WorkflowRun


class WorkflowRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, workflow_id: str) -> WorkflowRun | None:
        return await self.db.get(WorkflowRun, workflow_id)

    async def get_by_idempotency_key(self, key: str) -> WorkflowRun | None:
        result = await self.db.execute(
            select(WorkflowRun).where(WorkflowRun.idempotency_key == key)
        )
        return result.scalar_one_or_none()

    async def save(self, run: WorkflowRun) -> WorkflowRun:
        self.db.add(run)
        await self.db.commit()
        await self.db.refresh(run)
        return run
