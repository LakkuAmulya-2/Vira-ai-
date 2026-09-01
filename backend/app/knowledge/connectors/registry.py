from app.knowledge.connectors.base import SourceConnector


class ConnectorRegistry:
    def __init__(self) -> None:
        self._connectors: dict[str, SourceConnector] = {}

    def register(self, connector: SourceConnector) -> None:
        if connector.source_name in self._connectors:
            raise ValueError(f"Duplicate connector: {connector.source_name}")
        self._connectors[connector.source_name] = connector

    def get(self, source_name: str) -> SourceConnector:
        try:
            return self._connectors[source_name]
        except KeyError as exc:
            raise LookupError(f"Unknown connector: {source_name}") from exc
