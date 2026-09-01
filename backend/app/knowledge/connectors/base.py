from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.knowledge.contracts import CandidateClaimInput


class SourceConnector(ABC):
    source_name: str

    @abstractmethod
    async def collect(self) -> AsyncIterator[CandidateClaimInput]:
        """Yield normalized candidate claims from an approved source."""
        raise NotImplementedError
