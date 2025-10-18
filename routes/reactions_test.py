"""
Auto-generated tests using LLM and RAG
"""

import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import app  # ✅ CRITICAL: Import Flask app for client fixture
from routes.reactions import (
    add_reaction,
    remove_reaction,
    toggle_reaction,
    get_message_reactions,
    get_user_reactions,
    get_reaction_count,
    get_most_popular,
    get_allowed_emojis,
    bulk_add_reactions
)

@pytest.fixture
def client():
    """Flask test client with app context."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


# Skipped: require_auth is a decorator function
# Decorators are tested indirectly through the functions that use them
def test_require_auth_skipped():
    """Decorator require_auth is tested through its usage."""
    pass


class TestAddReaction:
    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_success(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.return_value = {'success': True}
        response = client.post('/api/reactions/add', headers={'X-User-ID': '123'}, json={'message_id': 1, 'emoji': '👍'})
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_missing_data(self, mock_reaction_manager, client):
        response = client.post('/api/reactions/add', headers={'X-User-ID': '123'}, json={})
        assert response.status_code == 400
        assert response.get_json() == {"error": "message_id and emoji are required"}

    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_failure(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.return_value = {'success': False}
        response = client.post('/api/reactions/add', headers={'X-User-ID': '123'}, json={'message_id': 1, 'emoji': '👍'})
        assert response.status_code == 400
        assert response.get_json() == {'success': False}

    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_value_error(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.side_effect = ValueError("Invalid emoji")
        response = client.post('/api/reactions/add', headers={'X-User-ID': '123'}, json={'message_id': 1, 'emoji': 'invalid'})
        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid emoji"}

    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_unexpected_error(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.side_effect = Exception("Unexpected error")
        response = client.post('/api/reactions/add', headers={'X-User-ID': '123'}, json={'message_id': 1, 'emoji': '👍'})
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to add reaction: Unexpected error"}


class TestRemoveReaction:
    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_success(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.return_value = {'success': True}
        response = client.post('/api/reactions/remove', headers={'X-User-ID': '123'}, json={
            'message_id': 1,
            'emoji': '👍'
        })
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_not_found(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.return_value = {'success': False}
        response = client.post('/api/reactions/remove', headers={'X-User-ID': '123'}, json={
            'message_id': 999,
            'emoji': '👍'
        })
        assert response.status_code == 404
        assert response.get_json() == {'success': False}

    def test_remove_reaction_missing_data(self, client):
        response = client.post('/api/reactions/remove', headers={'X-User-ID': '123'}, json={})
        assert response.status_code == 400
        assert response.get_json() == {"error": "message_id and emoji are required"}

    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_exception(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.side_effect = Exception("Unexpected error")
        response = client.post('/api/reactions/remove', headers={'X-User-ID': '123'}, json={
            'message_id': 1,
            'emoji': '👍'
        })
        assert response.status_code == 500
        assert "Failed to remove reaction" in response.get_json()["error"]


class TestToggleReaction:
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_success(self, mock_reaction_manager, client):
        mock_reaction_manager.toggle_reaction.return_value = {"success": True}
        response = client.post('/api/reactions/toggle', headers={'X-User-ID': '123'}, json={
            'message_id': 1,
            'emoji': '👍'
        })
        assert response.status_code == 200
        assert response.get_json() == {"success": True}

    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_missing_data(self, mock_reaction_manager, client):
        response = client.post('/api/reactions/toggle', headers={'X-User-ID': '123'}, json={})
        assert response.status_code == 400
        assert response.get_json() == {"error": "message_id and emoji are required"}

    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_value_error(self, mock_reaction_manager, client):
        mock_reaction_manager.toggle_reaction.side_effect = ValueError("Invalid emoji")
        response = client.post('/api/reactions/toggle', headers={'X-User-ID': '123'}, json={
            'message_id': 1,
            'emoji': 'invalid_emoji'
        })
        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid emoji"}

    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_unexpected_error(self, mock_reaction_manager, client):
        mock_reaction_manager.toggle_reaction.side_effect = Exception("Unexpected error")
        response = client.post('/api/reactions/toggle', headers={'X-User-ID': '123'}, json={
            'message_id': 1,
            'emoji': '👍'
        })
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to toggle reaction: Unexpected error"}


class TestGetMessageReactions:
    @patch('routes.reactions.reaction_manager.get_message_reactions')
    def test_get_message_reactions_success(self, mock_get_reactions, client):
        mock_get_reactions.return_value = {'👍': 5, '❤️': 3}
        response = client.get('/api/reactions/message/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message_id'] == 1
        assert data['reactions'] == {'👍': 5, '❤️': 3}

    @patch('routes.reactions.reaction_manager.get_message_reactions')
    def test_get_message_reactions_failure(self, mock_get_reactions, client):
        mock_get_reactions.side_effect = Exception("Database error")
        response = client.get('/api/reactions/message/1')
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == "Failed to get reactions: Database error"

    @pytest.mark.parametrize("message_id, expected_status", [
        (1, 200),
        (999, 200),
        (0, 200),
    ])
    @patch('routes.reactions.reaction_manager.get_message_reactions')
    def test_get_message_reactions_various_ids(self, mock_get_reactions, client, message_id, expected_status):
        mock_get_reactions.return_value = {}
        response = client.get(f'/api/reactions/message/{message_id}')
        assert response.status_code == expected_status
        data = response.get_json()
        assert data['success'] is True
        assert data['message_id'] == message_id
        assert data['reactions'] == {}


class TestGetUserReactions:
    @patch('routes.reactions.reaction_manager')
    def test_get_user_reactions_error(self, mock_reaction_manager, client):
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database error")
        response = client.get('/api/reactions/user', headers={'X-User-ID': '123'})
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert data['error'] == "Failed to get user reactions: Database error"

    def test_get_user_reactions_unauthorized(self, client):
        response = client.get('/api/reactions/user')
        assert response.status_code == 401


class TestGetReactionCount:
    @patch('routes.reactions.reaction_manager')
    def test_get_reaction_count_success(self, mock_reaction_manager, client):
        mock_reaction_manager.get_reaction_count.return_value = 5
        response = client.get('/api/reactions/count/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message_id'] == 1
        assert data['count'] == 5

    @patch('routes.reactions.reaction_manager')
    def test_get_reaction_count_failure(self, mock_reaction_manager, client):
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Database error")
        response = client.get('/api/reactions/count/1')
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Failed to get reaction count" in data['error']

    @pytest.mark.parametrize("message_id, expected_count", [
        (1, 10),
        (2, 0),
        (3, 15),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_get_reaction_count_various_ids(self, mock_reaction_manager, client, message_id, expected_count):
        mock_reaction_manager.get_reaction_count.return_value = expected_count
        response = client.get(f'/api/reactions/count/{message_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message_id'] == message_id
        assert data['count'] == expected_count


class TestGetMostPopular:
    @patch('routes.reactions.reaction_manager')
    def test_get_most_popular_success(self, mock_reaction_manager, client):
        mock_reaction_manager.get_most_popular_emoji.return_value = "👍"
        response = client.get('/api/reactions/popular/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message_id'] == 1
        assert data['most_popular_emoji'] == "👍"

    @patch('routes.reactions.reaction_manager')
    def test_get_most_popular_failure(self, mock_reaction_manager, client):
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Database error")
        response = client.get('/api/reactions/popular/1')
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Failed to get popular emoji" in data['error']


class TestGetAllowedEmojis:
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_success(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = ['👍', '❤️', '😂']
        response = client.get('/api/reactions/allowed-emojis')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['emojis'] == ['👍', '❤️', '😂']

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_empty(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = []
        response = client.get('/api/reactions/allowed-emojis')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['emojis'] == []


class TestBulkAddReactions:
    @patch('routes.reactions.reaction_manager')
    def test_bulk_add_reactions_success(self, mock_reaction_manager, client):
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 3}
        response = client.post('/api/reactions/bulk', headers={'X-User-ID': '123'}, json={
            "reactions": [
                {"message_id": 1, "user_id": 123, "emoji": "👍"},
                {"message_id": 2, "user_id": 123, "emoji": "❤️"},
                {"message_id": 3, "user_id": 123, "emoji": "😂"}
            ]
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['result'] == {"added": 3}

    def test_bulk_add_reactions_missing_reactions(self, client):
        response = client.post('/api/reactions/bulk', headers={'X-User-ID': '123'}, json={})
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == "reactions array is required"

    @patch('routes.reactions.reaction_manager')
    def test_bulk_add_reactions_exception(self, mock_reaction_manager, client):
        mock_reaction_manager.bulk_add_reactions.side_effect = Exception("Database error")
        response = client.post('/api/reactions/bulk', headers={'X-User-ID': '123'}, json={
            "reactions": [
                {"message_id": 1, "user_id": 123, "emoji": "👍"}
            ]
        })
        assert response.status_code == 500
        data = response.get_json()
        assert data['error'] == "Failed to bulk add reactions: Database error"