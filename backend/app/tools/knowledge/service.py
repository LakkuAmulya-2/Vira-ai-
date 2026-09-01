from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge import DataSource, KnowledgeClaim
from app.tools.knowledge.contracts import KnowledgeEvidence, KnowledgeSearchRequest, KnowledgeSearchResponse

async def search_verified_knowledge(
    db: AsyncSession, request: KnowledgeSearchRequest
) -> KnowledgeSearchResponse:
    terms = [term.strip() for term in request.query.split() if len(term.strip()) >= 2]
    statement = (
        select(KnowledgeClaim, DataSource)
        .join(DataSource, KnowledgeClaim.source_id == DataSource.id)
        .where(
            KnowledgeClaim.status == "VERIFIED",
            DataSource.verification_status == "VERIFIED",
        )
    )

    if request.entity_type:
        statement = statement.where(KnowledgeClaim.entity_type == request.entity_type)
    if request.country_code:
        statement = statement.where(KnowledgeClaim.country_code == request.country_code.upper())
    if request.jurisdiction:
        statement = statement.where(KnowledgeClaim.jurisdiction == request.jurisdiction)

    if terms:
        predicates = []
        for term in terms:
            pattern = f"%{term}%"
            predicates.extend([
                KnowledgeClaim.entity_type.ilike(pattern),
                KnowledgeClaim.entity_key.ilike(pattern),
                KnowledgeClaim.field.ilike(pattern),
            ])
        statement = statement.where(or_(*predicates))

    rows = (await db.execute(statement.limit(request.limit))).all()
    evidence = [
        KnowledgeEvidence(
            claim_id=claim.id,
            entity_type=claim.entity_type,
            entity_key=claim.entity_key,
            field=claim.field,
            value=claim.value,
            source_name=source.name,
            source_url=source.base_url,
            country_code=claim.country_code,
            jurisdiction=claim.jurisdiction,
        )
        for claim, source in rows
    ]
    return KnowledgeSearchResponse(query=request.query, evidence=evidence, total=len(evidence))
