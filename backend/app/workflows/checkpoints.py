from app.workflows.repository import WorkflowRepository
from app.workflows.persistence import WorkflowRun


async def checkpoint(
    repository: WorkflowRepository,
    run: WorkflowRun,
    *,
    status: str,
    current_step: str | None,
    state: dict,
    error: str | None = None,
) -> WorkflowRun:
    run.status = status
    run.current_step = current_step
    run.state = state
    run.error = error
    return await repository.save(run)
