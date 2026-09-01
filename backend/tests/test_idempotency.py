from app.workflows.idempotency import workflow_key


def test_workflow_key_is_stable():
    assert workflow_key("u1", "journey", "r1") == workflow_key("u1", "journey", "r1")
    assert workflow_key("u1", "journey", "r1") != workflow_key("u2", "journey", "r1")
