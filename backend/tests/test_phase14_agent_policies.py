import pytest
from app.agents.langgraph.policies import assert_tool_allowed
def test_allowed_tool():
 assert_tool_allowed("CAREER","knowledge.search") is None
def test_disallowed_tool():
 with pytest.raises(PermissionError):assert_tool_allowed("CAREER","external.submit")
