from app.copilot.actions import propose_actions
def test_high_impact_action_requires_confirmation():
 actions=propose_actions("Please submit and pay the application",{"applications":[]})
 assert any(x["requires_confirmation"] for x in actions)
def test_deadline_action():
 actions=propose_actions("check my application deadline",{"applications":[{"id":"1"}]})
 assert any(x["action_type"]=="PROACTIVE_SCAN" for x in actions)
