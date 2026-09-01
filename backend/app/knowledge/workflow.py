from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.connectors.registry import ConnectorRegistry
from app.knowledge.ingestion import ingest_candidate_claim


class KnowledgeIngestionWorkflow:
    def __init__(self, registry: ConnectorRegistry) -> None:
        self.registry = registry

    async def run(self, db: AsyncSession, source_name: str) -> int:
        connector = self.registry.get(source_name)
        accepted = 0
        async for claim in connector.collect():
            await ingest_candidate_claim(db, claim)
            accepted += 1
        return accepted
