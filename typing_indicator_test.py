"""
Auto-generated tests using LLM and RAG
"""

from datetime import datetime, timedelta
from typing_indicator import TypingIndicator
import pytest


def test_generation_failed():
    """Test generation produced unfixable syntax errors - placeholder only."""
    pytest.skip(
        "Generated test had syntax errors that could not be fixed after all attempts")


@pytest.fixture
def typing_indicator():
    return TypingIndicator()


@pytest.mark.parametrize("initial_state, room_id, user_id, expected_state", [
    # Happy path: user is typing and stops
    ({"room1": {"user1": {"username": "Alice", "started_at": datetime.now()}}},
     "room1", "user1", {}),
    # Error case: user is not typing
    ({"room1": {}}, "room1", "user1", {}),
    # Edge case: room does not exist
    ({}, "room2", "user1", {}),
    # Edge case: multiple users, one stops typing
    ({"room1": {"user1": {"username": "Alice", "started_at": datetime.now()},
                "user2": {"username": "Bob", "started_at": datetime.now()}}}, "room1", "user1",
     {"user2": {"username": "Bob", "started_at": datetime.now()}}),
])
def test_user_stopped_typing(
        typing_indicator,
        initial_state,
        room_id,
        user_id,
        expected_state):
    typing_indicator.typing_users = initial_state
    typing_indicator.user_stopped_typing(room_id, user_id)
    assert typing_indicator.typing_users.get(room_id, {}) == expected_state


@pytest.fixture
def typing_indicator():
    return TypingIndicator()


@pytest.mark.parametrize("room_id, typing_data, expected", [
    ("room1", {}, []),  # No users typing
    ("room1", {
        "user1": {"username": "Alice", "started_at": datetime.now() - timedelta(seconds=3)}
    }, [{"user_id": "user1", "username": "Alice"}]),  # User typing within 5 seconds
    ("room1", {
        "user1": {"username": "Alice", "started_at": datetime.now() - timedelta(seconds=6)}
    }, []),  # User typing expired
])
def test_get_typing_users(typing_indicator, room_id, typing_data, expected):
    typing_indicator.typing_users[room_id] = typing_data
    assert typing_indicator.get_typing_users(room_id) == expected


def test_get_typing_users_no_room(typing_indicator):
    assert typing_indicator.get_typing_users("non_existent_room") == []


@pytest.mark.parametrize("room_id, typing_data, expected", [
    ("room1", {
        "user1": {"username": "Alice", "started_at": datetime.now() - timedelta(seconds=4)},
        "user2": {"username": "Bob", "started_at": datetime.now() - timedelta(seconds=6)}
    }, [{"user_id": "user1", "username": "Alice"}]),  # Mixed active and expired users
])
def test_get_typing_users_mixed(
        typing_indicator,
        room_id,
        typing_data,
        expected):
    typing_indicator.typing_users[room_id] = typing_data
    assert typing_indicator.get_typing_users(room_id) == expected
