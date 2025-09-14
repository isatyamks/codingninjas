from src.interview.state import new_session, Session

def test_new_session():
    session = new_session("TestUser", "entry")
    assert isinstance(session, Session)
    assert session.candidate_name == "TestUser"
    assert session.level == "entry"
    assert session.current_q_idx == 0
    assert session.qa == []
    assert session.scores == []
    assert session.transcript == []
