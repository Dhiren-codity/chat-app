"""
Auto-generated tests using LLM and RAG
"""

from reaction_manager import ReactionManager
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def reaction_manager():
    return ReactionManager()


@pytest.mark.parametrize("user_id, message_id", [
    (None, None),
    ("invalid_id", 101)
])
def test_get_user_reactions_invalid_user_id(
        reaction_manager, user_id, message_id):
    with pytest.raises(Exception):
        reaction_manager.get_user_reactions(user_id, message_id)


@pytest.mark.parametrize("message_id, expected_count", [
    (1, 5),  # Happy path: message with 5 reactions
    (2, 0),  # Edge case: message with 0 reactions
    (3, 1),  # Edge case: message with 1 reaction
])
def test_get_reaction_count_happy_path(
        reaction_manager,
        message_id,
        expected_count):
    # Mock the query and count method
    MessageReaction = MagicMock()
    MessageReaction.query.filter_by.return_value.count.return_value = expected_count
    # Inject the mock into the method
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('reaction_manager.MessageReaction', MessageReaction)
        assert reaction_manager.get_reaction_count(
            message_id) == expected_count


def test_get_reaction_count_error_case(reaction_manager):
    # Mock the query to raise an exception
    MessageReaction = MagicMock()
    MessageReaction.query.filter_by.side_effect = Exception("Database error")
    # Inject the mock into the method
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('reaction_manager.MessageReaction', MessageReaction)
        with pytest.raises(Exception, match="Database error"):
            reaction_manager.get_reaction_count(999)


@pytest.mark.parametrize("reactions, expected", [
    # Edge case: empty list of reactions
    (
        [],
        {'total': 0, 'added': 0, 'failed': 0, 'errors': []}
    ),
    # Edge case: all reactions fail due to disallowed emojis
    (
        [
            {'message_id': 1, 'user_id': 1, 'emoji': '🚀'},
            {'message_id': 2, 'user_id': 2, 'emoji': '🌟'}
        ],
        {'total': 2, 'added': 0, 'failed': 2, 'errors': [
            "Emoji '🚀' not allowed. Allowed: 👍, ❤️, 😂, 😮, 😢, 🎉, 🔥, 👏",
            "Emoji '🌟' not allowed. Allowed: 👍, ❤️, 😂, 😮, 😢, 🎉, 🔥, 👏"
        ]}
    ),
])
def test_bulk_add_reactions(reaction_manager, reactions, expected):
    result = reaction_manager.bulk_add_reactions(reactions)
    assert result == expected


@pytest.mark.parametrize("expected_emojis", [
    (['👍', '❤️', '😂', '😮', '😢', '🎉', '🔥', '👏']),
])
def test_get_allowed_emojis_happy_path(reaction_manager, expected_emojis):
    assert reaction_manager.get_allowed_emojis() == expected_emojis


@pytest.mark.parametrize("modify_emojis", [
    (['👍', '❤️', '😂']),
])
def test_get_allowed_emojis_edge_case_modification(
        reaction_manager, modify_emojis):
    emojis = reaction_manager.get_allowed_emojis()
    emojis.append('😎')
    assert emojis != reaction_manager.get_allowed_emojis()


@pytest.mark.parametrize("expected_length", [
    (8),
])
def test_get_allowed_emojis_edge_case_length(
        reaction_manager, expected_length):
    assert len(reaction_manager.get_allowed_emojis()) == expected_length


@pytest.mark.parametrize("expected_type", [
    (list),
])
def test_get_allowed_emojis_type(reaction_manager, expected_type):
    assert isinstance(reaction_manager.get_allowed_emojis(), expected_type)


@pytest.mark.parametrize("expected_empty", [
    (False),
])
def test_get_allowed_emojis_not_empty(reaction_manager, expected_empty):
    assert bool(reaction_manager.get_allowed_emojis()) is not expected_empty
