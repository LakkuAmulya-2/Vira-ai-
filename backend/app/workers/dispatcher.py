from app.workers.contracts import BackgroundJob


class JobDispatcher:
    async def enqueue(self, job: BackgroundJob) -> None:
        raise NotImplementedError(
            "Configure a production queue adapter (Redis/Celery/Arq) through deployment settings."
        )
