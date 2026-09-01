from app.agents.langgraph.graph import ViraLangGraph
def test_graph_has_runtime():
    assert ViraLangGraph().graph is not None
