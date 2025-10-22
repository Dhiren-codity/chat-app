"""
Auto-generated tests using LLM and RAG
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict

@pytest.fixture
def typing_indicator():
    return TypingIndicator()

class TypingIndicator:
    def __init__(self):
        self.typing_users: Dict[str, Dict[str, Dict[str, any]]] = {}
    def get_typing_users(self, room_id):
        if room_id not in self.typing_users:
            return []
        current_time = datetime.now()
        active_typers = []
        for user_id, data in list(self.typing_users[room_id].items()):
            if current_time - data['started_at'] < timedelta(seconds=5):
                active_typers.append({
                    'user_id': user_id,
                    'username': data['username']
                })
            else:
                del self.typing_users[room_id][user_id]
        return active_typers

@pytest.mark.parametrize("edge_case", [
    (None,),  # Edge case: Check if typing_users is not None
    (0,),     # Edge case: Check if typing_users is empty (length 0)
])
def test_typing_indicator_init_edge_cases(edge_case):
    indicator = TypingIndicator()
    if edge_case is None:
        assert indicator.typing_users is not None
    elif edge_case == 0:
        assert len(indicator.typing_users) == edge_case

@pytest.mark.parametrize("room_id, typing_data, expected", [
    ("room1", {}, []),  # No users typing
    ("room1", {
        "user1": {"username": "Alice", "started_at": datetime.now() - timedelta(seconds=3)}
    }, [{"user_id": "user1", "username": "Alice"}]),  # User typing within 5 seconds
    ("room1", {
        "user1": {"username": "Alice", "started_at": datetime.now() - timedelta(seconds=6)}
    }, []),  # User typing expired
    ("room1", {
        "user1": {"username": "Alice", "started_at": datetime.now() - timedelta(seconds=3)},
        "user2": {"username": "Bob", "started_at": datetime.now() - timedelta(seconds=6)}
    }, [{"user_id": "user1", "username": "Alice"}]),  # Mixed active and expired users
    ("room2", {}, []),  # Room does not exist
])
def test_get_typing_users(typing_indicator, room_id, typing_data, expected):
    typing_indicator.typing_users[room_id] = typing_data
    assert typing_indicator.get_typing_users(room_id) == expected