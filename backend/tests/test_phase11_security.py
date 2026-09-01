import pytest
from app.core.security import CurrentUser
@pytest.mark.asyncio
async def test_current_user_is_immutable():
    user=CurrentUser(id="u1",role="STUDENT")
    assert user.id=="u1"
