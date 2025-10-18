"""
Auto-generated tests using LLM and RAG
"""

import pytest


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



from unittest.mock import patch
from app import app  # ✅ CRITICAL: Import Flask app for client fixture
from routes.reactions import add_reaction

class TestAddReaction:
    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_success(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.return_value = {'success': True}

        response = client.post('/api/reactions/add', headers={'X-User-ID': '123'}, json={
            'message_id': 1,
            'emoji': '👍'
        })

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

        response = client.post('/api/reactions/add', headers={'X-User-ID': '123'}, json={
            'message_id': 1,
            'emoji': '👍'
        })

        assert response.status_code == 400
        assert response.get_json() == {'success': False}

    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_value_error(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.side_effect = ValueError("Invalid emoji")

        response = client.post('/api/reactions/add', headers={'X-User-ID': '123'}, json={
            'message_id': 1,
            'emoji': 'invalid_emoji'
        })

        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid emoji"}

    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_unexpected_error(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.side_effect = Exception("Unexpected error")

        response = client.post('/api/reactions/add', headers={'X-User-ID': '123'}, json={
            'message_id': 1,
            'emoji': '👍'
        })

        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to add reaction: Unexpected error"}


from routes.reactions import remove_reaction

class TestRemoveReaction:
    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_success(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.return_value = {'success': True}
        response = client.post('/api/reactions/remove', headers={'X-User-ID': '123'}, json={'message_id': 1, 'emoji': '👍'})
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_not_found(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.return_value = {'success': False}
        response = client.post('/api/reactions/remove', headers={'X-User-ID': '123'}, json={'message_id': 1, 'emoji': '👍'})
        assert response.status_code == 404
        assert response.get_json() == {'success': False}

    def test_remove_reaction_missing_data(self, client):
        response = client.post('/api/reactions/remove', headers={'X-User-ID': '123'}, json={})
        assert response.status_code == 400
        assert response.get_json() == {"error": "message_id and emoji are required"}

    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_exception(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.side_effect = Exception("Unexpected error")
        response = client.post('/api/reactions/remove', headers={'X-User-ID': '123'}, json={'message_id': 1, 'emoji': '👍'})
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to remove reaction: Unexpected error"}


from routes.reactions import toggle_reaction

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
            'emoji': 'invalid'
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

    @pytest.mark.parametrize("headers, json_data, expected_status, expected_response", [
        ({'X-User-ID': '123'}, {'message_id': 1, 'emoji': '👍'}, 200, {"success": True}),
        ({'X-User-ID': '123'}, {}, 400, {"error": "message_id and emoji are required"}),
        ({}, {'message_id': 1, 'emoji': '👍'}, 401, None),  # Assuming 401 for missing auth
    ])
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_various_cases(self, mock_reaction_manager, client, headers, json_data, expected_status, expected_response):
        mock_reaction_manager.toggle_reaction.return_value = {"success": True}

        response = client.post('/api/reactions/toggle', headers=headers, json=json_data)

        assert response.status_code == expected_status
        if expected_response is not None:
            assert response.get_json() == expected_response


from routes.reactions import get_user_reactions

class TestGetUserReactions:
    @patch('routes.reactions.reaction_manager')
    def test_get_user_reactions_failure(self, mock_reaction_manager, client):
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database error")

        response = client.get('/api/reactions/user', headers={'X-User-ID': '123'})

        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert data['error'] == "Failed to get user reactions: Database error"

    def test_get_user_reactions_unauthorized(self, client):
        response = client.get('/api/reactions/user')

        assert response.status_code == 401


from routes.reactions import get_reaction_count

class TestGetReactionCount:
    @patch('routes.reactions.reaction_manager')
    def test_get_reaction_count_success(self, mock_reaction_manager, client):
        # Setup mock
        mock_reaction_manager.get_reaction_count.return_value = 5

        # Make request
        response = client.get('/api/reactions/count/1')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message_id'] == 1
        assert data['count'] == 5

    @patch('routes.reactions.reaction_manager')
    def test_get_reaction_count_failure(self, mock_reaction_manager, client):
        # Setup mock to raise an exception
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Database error")

        # Make request
        response = client.get('/api/reactions/count/1')

        # Assert
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == "Failed to get reaction count: Database error"

    @pytest.mark.parametrize("message_id, expected_count", [
        (1, 10),
        (2, 0),
        (3, 15),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_get_reaction_count_various_ids(self, mock_reaction_manager, client, message_id, expected_count):
        # Setup mock
        mock_reaction_manager.get_reaction_count.return_value = expected_count

        # Make request
        response = client.get(f'/api/reactions/count/{message_id}')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message_id'] == message_id
        assert data['count'] == expected_count


from routes.reactions import get_most_popular

class TestGetMostPopular:
    @patch('routes.reactions.reaction_manager')
    def test_get_most_popular_happy_path(self, mock_reaction_manager, client):
        mock_reaction_manager.get_most_popular_emoji.return_value = "👍"

        response = client.get('/api/reactions/popular/1')

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message_id'] == 1
        assert data['most_popular_emoji'] == "👍"

    @patch('routes.reactions.reaction_manager')
    def test_get_most_popular_error_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Database error")

        response = client.get('/api/reactions/popular/1')

        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert data['error'] == "Failed to get popular emoji: Database error"


from routes.reactions import get_allowed_emojis

class TestGetAllowedEmojis:
    @patch('routes.reactions.ReactionManager')
    def test_get_allowed_emojis_success(self, mock_reaction_manager, client):
        # Setup mock
        mock_reaction_manager.get_allowed_emojis.return_value = ['👍', '❤️', '😂']

        # Make request
        response = client.get('/api/reactions/allowed-emojis')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['emojis'] == ['👍', '❤️', '😂']

    @patch('routes.reactions.ReactionManager')
    def test_get_allowed_emojis_empty(self, mock_reaction_manager, client):
        # Setup mock
        mock_reaction_manager.get_allowed_emojis.return_value = []

        # Make request
        response = client.get('/api/reactions/allowed-emojis')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['emojis'] == []


from routes.reactions import bulk_add_reactions

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
