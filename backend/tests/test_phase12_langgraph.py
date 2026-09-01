from app.agents.langgraph.graph import ViraLangGraph
def test_langgraph_compiles():
 runtime=ViraLangGraph()
 assert runtime.graph is not None
